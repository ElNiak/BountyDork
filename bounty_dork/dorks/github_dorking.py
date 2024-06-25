#########################################################################################
# Github Dorking and searching functions
#########################################################################################

# Token Round Robin for Sequential Requests
from datetime import datetime
import random
import time

from bs4 import BeautifulSoup
import requests
from termcolor import cprint

from utils.app_config import *

token_index = 0

# GitHub Dorking
GITHUB_API_URL = "https://api.github.com"
TOKENS_LIST = ["your_github_token"]  # Add your GitHub tokens here
DORK_LIST = ["example_dork1", "example_dork2"]  # Add your dorks here
QUERIES_LIST = ["example_query"]  # Add your queries here
ORGANIZATIONS_LIST = ["example_organization"]  # Add your organizations here
USERS_LIST = ["example_user"]  # Add your users here


def token_round_robin():
    global token_index
    token = TOKENS_LIST[token_index]
    token_index = (token_index + 1) % len(TOKENS_LIST)
    return token


# URL Encoding Function
def __urlencode(str):
    return str.replace(":", "%3A").replace('"', "%22").replace(" ", "+")


def rate_limit_handler(headers):
    if "X-RateLimit-Reset" in headers:
        reset_time = datetime.fromtimestamp(int(headers["X-RateLimit-Reset"]))
        wait_time = (
            reset_time - datetime.now()
        ).total_seconds() + 10  # Adding 10 seconds buffer
        print(f"Rate limit hit. Waiting for {wait_time} seconds.")
        time.sleep(wait_time)


def get_rate_limit_status():
    headers = {"Authorization": f"token {token_round_robin()}"}
    response = requests.get(f"{GITHUB_API_URL}/rate_limit", headers=headers)
    if response.status_code == 200:
        rate_limit = response.json()["rate"]
        print(
            f"Limit: {rate_limit['limit']}, Remaining: {rate_limit['remaining']}, Reset: {datetime.fromtimestamp(rate_limit['reset'])}"
        )
    else:
        print("Failed to fetch rate limit status")


# TODO
def github_search_with_proxy(dork_tuple, proxy, category, retries=3, advanced=False):
    # TODO advanced search
    try:
        query, extension = dork_tuple
    except ValueError:
        query = dork_tuple
        extension = ""
    full_query = f"{query} {extension}".strip()
    base_url = f"{GITHUB_API_URL}/search/code?q=" + __urlencode(extension + " " + query)
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Authorization": f"token {token_round_robin()}",
    }
    proxies = {"http": proxy, "https": proxy}
    urls = []
    for _ in range(retries):
        try:
            cprint(
                f"Searching for {full_query} ({category}) with proxy {proxy}...",
                "yellow",
                file=sys.stderr,
            )
            response = requests.get(
                base_url, headers=headers, params=params, proxies=proxies, timeout=10
            )

            # Parse
            soup = BeautifulSoup(response.text, "html.parser")
            result_block = soup.find_all("div", attrs={"class": "g"})
            for result in result_block:
                # Find link, title, description
                link = result.find("a", href=True)
                title = result.find("h3")
                description_box = result.find("div", {"style": "-webkit-line-clamp:2"})
                if description_box:
                    description = description_box.text
                    if link and title and description:
                        if advanced:
                            urls.append(
                                SearchResult(link["href"], title.text, description)
                            )
                        else:
                            urls.append(link["href"])

            # Placeholder for URL extraction logic
            return category, urls  # Return the category and a placeholder result
        except requests.exceptions.RequestException as e:
            # cprint(f"Error searching for {full_query} with proxy {proxy}: {e}", 'red', file=sys.stderr)
            time.sleep(2)  # Wait before retrying

    return category, None  # Indicate failure after retries


# def launch_github_dorks_and_search_attack(extension=DEFAULT_EXTENSION, total_output=DEFAULT_TOTAL_OUTPUT, page_no=DEFAULT_PAGE_NO, proxies=None):
#     pass
