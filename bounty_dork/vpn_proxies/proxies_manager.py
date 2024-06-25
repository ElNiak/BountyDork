#########################################################################################
# Proxy related functions
#########################################################################################

# Round-robin proxy generator
import csv
import itertools
import json
import os
import random
import threading
import time

import requests
from termcolor import cprint
import concurrent.futures
from tqdm import tqdm
from typing import List, Literal
import sys

from utils.app_config import USER_AGENTS
from fp.fp import FreeProxy, FreeProxyException


def round_robin_proxies(proxies):
    return itertools.cycle(proxies)


# Function to check if a proxy is up
def is_proxy_alive(proxy, config, retry=0):
    """
    Check if a proxy is alive by sending a test request to Google.

    Args:
        proxy (str): The proxy to test.
        config (dict): Configuration settings.
        retry (int, optional): The number of retry attempts. Defaults to 0.

    Returns:
        tuple: A tuple containing a boolean indicating if the proxy is alive and the proxy itself.
    """
    try:
        cprint(
            f"Testing proxy {proxy}, retry n° {retry} ...",
            "yellow",
            file=sys.stderr,
        )
        # TODO use request_manager
        response = requests.get(
            "http://www.google.com/search?q=test",
            proxies={"http": proxy, "https": proxy},
            timeout=config["proxy_mean_delay"],
            headers={"User-Agent": random.choice(USER_AGENTS)},
            verify=False,
        )
        if response and response.status_code == 429 and retry < 3:
            retry_after = int(response.headers.get("Retry-After", 60))
            cprint(
                f"Proxy {proxy}: Retry after {retry_after} secs ...",
                "red",
                file=sys.stderr,
            )
            time.sleep(retry_after)
            return is_proxy_alive(proxy=proxy, retry=retry + 1, config=config)
        return response.status_code == 200, proxy
    except requests.exceptions.RequestException as e:
        cprint(
            f"Proxy {proxy} error with : {e}",
            "red",
            file=sys.stderr,
        )
        return False, proxy


# Load proxies from file
def load_proxies(file="vpn_proxies/proxies/free-proxy-list.txt"):
    with open(file, "r") as file:
        return [line.strip() for line in file if line.strip()]


def remove_unavailable_proxies(proxies: List[str], config: dict) -> List[str]:
    raise NotImplementedError("This function is not implemented yet.")


def prepare_proxies(proxy, config):
    if proxy and "username:password" in proxy:
        nord_vpn_user_pass = random.choice(config["nord_vpn_login"])
        proxy = proxy.replace("username", nord_vpn_user_pass[0]).replace(
            "password", nord_vpn_user_pass[1]
        )
        proxies = {"https": proxy}

    else:
        if not "http" in proxy or not "socks" in proxy:
            proxy = "http://" + proxy
        proxies = {"http": proxy, "https": proxy}
    return proxies


def get_proxies_and_cycle(config):
    """Get proxies and proxy cycle.

    This function retrieves the proxies from the configuration and sets up a proxy cycle.
    If the configuration specifies the use of a proxy, it checks if there are any proxies available.
    If no proxies are available and the use of a proxy is required, it prints an error message and exits.
    If the use of a proxy is not required, it sets the proxies list to contain a single None value.
    Finally, it sets up a proxy cycle using the retrieved proxies and returns both the proxies list and the proxy cycle.

    Args:
        config (dict): The configuration dictionary containing the proxy settings.

    Returns:
        tuple: A tuple containing the proxies list and the proxy cycle.
    """
    proxies = config["proxies"]
    if config["use_proxy"] and len(proxies) == 0:
        cprint(
            f"Using proxies -> you should have at least one UP",
            "red",
            file=sys.stderr,
        )
        exit()

    if not config["use_proxy"]:
        proxies = [None]

    proxy_cycle = round_robin_proxies(proxies)
    return proxies, proxy_cycle


def setup_proxies(config):
    """Set up proxies based on the provided configuration.

    Args:
        config (dict): A dictionary containing the configuration options.

    Returns:
        None
    """
    proxies = []
    if config["use_free_proxy_file"]:
        cprint("Loading proxies from file ...", "yellow", file=sys.stderr)
        proxies = load_proxies()
        proxies_cp = proxies.copy()
        dead_proxies = 0
        total_proxies = len(proxies)

        lock = threading.Lock()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_search = {
                executor.submit(is_proxy_alive, proxy, config, 0): proxy
                for proxy in proxies_cp
            }
            for future in tqdm(
                concurrent.futures.as_completed(future_to_search),
                total=len(future_to_search),
                desc="Checking proxies",
                unit="proxy",
                leave=True,
                position=0,
            ):
                result = future.result()
                if result:
                    with lock:
                        if not result[0]:
                            dead_proxies += 1
                            cprint(
                                f"Removing dead proxy {result[1]}, dead proxies {dead_proxies}/{total_proxies}",
                                "red",
                                file=sys.stderr,
                            )
                            proxies.remove(result[1])
            cprint(f"Up free proxies: {len(proxies)}")

    if config["use_free_proxy"]:
        cprint("Using Free proxies ", "yellow", file=sys.stderr)
        try:
            free_proxy = FreeProxy(
                google=None, rand=True, https=True, timeout=10
            ).get_proxy_list(repeat=False)
            proxies += free_proxy
        except FreeProxyException as e:
            cprint(f"FreeProxyException: {e}", "red", file=sys.stderr)

    if config["use_nordvpn_proxy"]:
        config["nord_vpn_login"] = json.loads(config["nord_vpn_login"])
        cprint("Using NordVPN proxies ", "yellow", file=sys.stderr)
        if os.path.exists("vpn_proxies/proxies/nordvpn_login.csv"):
            with open("vpn_proxies/proxies/nordvpn_login.csv", "r") as file:
                nordvpn = list(csv.reader(file))
                for i in range(1, len(nordvpn)):
                    config["nord_vpn_login"].append([nordvpn[i][0], nordvpn[i][1]])
                cprint(
                    f"You have NordVPN account using these proxies {config['nord_vpn_login']}",
                    "green",
                    file=sys.stderr,
                )
            # https://stackoverflow.com/questions/64516109/how-to-use-nordvpn-servers-as-proxy-for-python-requests
            # TODO: curl -s https://nordvpn.com/api/server | jq -r ".[] | select(.features.socks==true) | [.domain, .name] | @tsv"
            with open("vpn_proxies/proxies/nordvpn-proxy-list.txt", "r") as file:
                for line in file.readlines():
                    line = line.replace("\n", "")
                    cprint(f"NordVPN Proxy: {line}", "yellow", file=sys.stderr)
                    p = (
                        "socks5h://"  # socks5h enable hostname resolution
                        + "username"
                        + ":"
                        + "password"
                        + "@"
                        + line
                        + ":1080"
                    )
                    proxies += [p]
        else:
            cprint(
                "You need to provide your NordVPN login details in proxies/nordvpn_login.csv",
                "red",
                file=sys.stderr,
            )
    config["proxies"] = list(set(proxies))
    cprint(f"Proxy: {config['proxies']}", "green", file=sys.stderr)


# TODO: https://stackoverflow.com/questions/55872164/how-to-rotate-proxies-on-a-python-requests
