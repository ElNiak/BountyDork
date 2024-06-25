import json
import random
import re
import sys
import time
from urllib.parse import parse_qs, urlparse

import requests
from termcolor import cprint

from utils.app_config import USER_AGENTS


def headers_403_bypass():
    """_summary_
    https://x.com/bountywriteups/status/1802974307036868838
    Returns:
        _type_: _description_
    """
    headers = {
        "Base-Url": "127.0.0.1",
        "Client-IP": "127.0.0.1",
        "Http-Url": "127.0.0.1",
        "Proxy-Host": "127.0.0.1",
        "Proxy-Url": "127.0.0.1",
        "Real-Ip": "127.0.0.1",
        "Redirect": "127.0.0.1",
        "Referer": "127.0.0.1",
        "Referrer": "127.0.0.1",
        "Refferer": "127.0.0.1",
        "Request-Uri": "127.0.0.1",
        "Uri": "127.0.0.1",
        "Url": "127.0.0.1",
        "X-Client-IP": "127.0.0.1",
        "X-Custom-IP-Authorization": "127.0.0.1",
        "X-Forward-For": "127.0.0.1",
        "X-Forwarded-By": "127.0.0.1",
        "X-Forwarded-For-Original": "127.0.0.1",
        "X-Forwarded-For": "127.0.0.1",
        "X-Forwarded-Host": "127.0.0.1",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Port": "4443",
        "X-Forwarded-Port": "80",
        "X-Forwarded-Port": "8080",
        "X-Forwarded-Port": "8443",
        "X-Forwarded-Scheme": ["http", "https"],
        "X-Forwarded-Server": "127.0.0.1",
        "X-Forwarded": "127.0.0.1",
        "X-Forwarder-For": "127.0.0.1",
        "X-Host": "127.0.0.1",
        "X-Http-Destinationurl": "127.0.0.1",
        "X-Http-Host-Override": "127.0.0.1",
        "X-Original-Remote-Addr": "127.0.0.1",
        "X-Original-Url": "127.0.0.1",
        "X-Originating-IP": "127.0.0.1",
        "X-Proxy-Url": "127.0.0.1",
        "X-Real-Ip": "127.0.0.1",
        "X-Remote-Addr": "127.0.0.1",
        "X-Remote-IP": "127.0.0.1",
        "X-Rewrite-Url": "127.0.0.1",
        "X-True-IP": "127.0.0.1",
    }
    return headers


# Function to check if a given URL has a query string
def has_query_string(url):
    return bool(urlparse.urlparse(url).query)


# Function to inject a payload into a given URL
def inject_payload(url, payload):
    if has_query_string(url):
        url_parts = list(urlparse.urlparse(url))
        query = dict(parse_qs(url_parts[4]))
        for key in query:
            query[key] = f"{query[key]}{payload}"
        url_parts[4] = urlparse.urlencode(query)
        url = urlparse.urlunparse(url_parts)
    else:
        url += f"{payload}"
    return url


def inject_params(url, payload):
    """
    Injects the payload in the parameters and returns a set
    """
    injected_url = set()
    temp_payload = (
        payload.replace("\\n", "$").replace("\\t", "@").replace("\\r", "!")
    )  # saves the payload from the removal of \\n, \\t and \\r
    injected = re.sub(r"=[^?\|&]*", "=" + str(temp_payload), str(url))
    final_payload = injected.replace("$", "\\n").replace("@", "\\t").replace("!", "\\r")
    injected_url.add(final_payload)

    return injected_url


def param_converter(data, url=False):
    if "str" in str(type(data)):
        if url:
            dictized = {}
            parts = data.split("/")[3:]
            for part in parts:
                dictized[part] = part
            return dictized
        else:
            return json.loads(data)
    else:
        if url:
            # url = urlparse(url).scheme + "://" + urlparse(url).netloc
            url = url + "?"
            for key in data.keys():
                url += key + "=" + str(data[key]) + "&"
            return url
        else:
            return json.dumps(data)


def get_url(url, GET):
    if GET:
        return url.split("?")[0]
    else:
        return url


def escaped(position, string):
    usable = string[:position][::-1]
    match = re.search(r"^\\*", usable)
    if match:
        match = match.group()
        if len(match) == 1:
            return True
        elif len(match) % 2 == 0:
            return False
        else:
            return True
    else:
        return False


def is_bad_context(position, non_executable_contexts):
    badContext = ""
    for each in non_executable_contexts:
        if each[0] < position < each[1]:
            badContext = each[2]
            break
    return badContext


xsschecker = "v3dm0s"


def replace_value(mapping, old, new, strategy=None):
    """
    Replace old values with new ones following dict strategy.

    The parameter strategy is None per default for inplace operation.
    A copy operation is injected via strateg values like copy.copy
    or copy.deepcopy

    Note: A dict is returned regardless of modifications.
    """
    anotherMap = strategy(mapping) if strategy else mapping
    if old in anotherMap.values():
        for k in anotherMap.keys():
            if anotherMap[k] == old:
                anotherMap[k] = new
    return anotherMap


def js_extractor(response):
    """Extract js files from the response body"""
    scripts = []
    matches = re.findall(r"<(?:script|SCRIPT).*?(?:src|SRC)=([^\s>]+)", response)
    for match in matches:
        if xsschecker in match:
            match = match.replace("'", "").replace('"', "").replace("`", "")
            scripts.append(match)
    return scripts


def stripper(string, substring, direction="right"):
    done = False
    strippedString = ""
    if direction == "right":
        string = string[::-1]
    for char in string:
        if char == substring and not done:
            done = True
        else:
            strippedString += char
    if direction == "right":
        strippedString = strippedString[::-1]
    return strippedString


def fill_holes(original, new):
    filler = 0
    filled = []
    for x, y in zip(original, new):
        if int(x) == (y + filler):
            filled.append(y)
        else:
            filled.extend([0, y])
            filler += int(x) - y
    return filled


def de_json(data):
    return data.replace("\\\\", "\\")


def handle_anchor(parent_url, url):
    """
    Constructs a complete URL based on the parent URL and the given URL.

    Args:
        parent_url (str): The parent URL.
        url (str): The URL to be handled.

    Returns:
        str: The complete URL.

    """
    scheme = urlparse(parent_url).scheme
    if url[:4] == "http":
        return url
    elif url[:2] == "//":
        return scheme + ":" + url
    elif url.startswith("/"):
        host = urlparse(parent_url).netloc
        scheme = urlparse(parent_url).scheme
        parent_url = scheme + "://" + host
        return parent_url + url
    elif parent_url.endswith("/"):
        return parent_url + url
    else:
        return parent_url + "/" + url


def get_params(url, data, GET):
    """Get the parameters from the given URL and data.

    This function parses the URL and data to extract the parameters and returns them as a dictionary.

    Args:
        url (str): The URL string.
        data (str): The data string.
        GET (str): The GET string.

    Returns:
        dict: A dictionary containing the extracted parameters.
    """
    params = {}
    if "?" in url and "=" in url:
        data = url.split("?")[1]
        if data[:1] == "?":
            data = data[1:]
    elif data:
        if False:  # TODO: get_var('jsonData') or get_var('path'):
            params = data
        else:
            try:
                params = json.loads(data.replace("'", '"'))
                return params
            except json.decoder.JSONDecodeError:
                pass
    else:
        return None
    if not params:
        parts = data.split("&")
        for part in parts:
            each = part.split("=")
            if len(each) < 2:
                each.append("")
            try:
                params[each[0]] = each[1]
            except IndexError:
                params = None
    return params


def start_request(
    proxies,
    config,
    is_json=False,
    GET=False,
    data=None,
    headers=None,
    params=None,
    base_url=None,
    secured=False,
    cookies=None,
    session=None,
    bypassed_403=False,
):
    """
    Send a HTTP request to the specified URL.

    Args:
        proxies (dict): A dictionary of proxy settings.
        config (dict): A dictionary of configuration settings.
        is_json (bool, optional): Indicates whether the request data is in JSON format. Defaults to False.
        GET (bool, optional): Indicates whether the request method is GET. Defaults to False.
        data (dict or str, optional): The request data. Defaults to None.
        headers (dict, optional): A dictionary of request headers. Defaults to None.
        params (dict, optional): A dictionary of request parameters. Defaults to None.
        base_url (str, optional): The base URL for the request. Defaults to None.
        secured (bool, optional): Indicates whether the request should be verified using SSL/TLS. Defaults to False.
        cookies (dict, optional): A dictionary of request cookies. Defaults to None.
        session (object, optional): A session object to use for the request. Defaults to None.

    Returns:
        object: The response object returned by the request.
    """
    if session:
        requester = session
    else:
        requester = requests
    try:
        if GET:
            response = requester.get(
                base_url,
                headers=headers,
                params=params,
                allow_redirects=True,
                proxies=proxies,
                # cookies = {'CONSENT' : 'YES+'},
                cookies=cookies,  # FOR EU USERS -> ANNOYING to parse
                verify=secured,  # TODO add parameter for that
                timeout=config["request_delay"],
            )
        elif is_json:
            response = requester.post(
                base_url,
                json=data[0],
                headers=headers,
                timeout=config["request_delay"],
                verify=secured,
                cookies=cookies,  # FOR EU USERS
                proxies=proxies,
            )
        else:
            response = requester.post(
                base_url,
                data=data[0],
                headers=headers,
                timeout=config["request_delay"],
                verify=secured,
                cookies=cookies,  # FOR EU USERS
                proxies=proxies,
            )

        # Parse Google response
        if response.status_code != 200:
            cprint(
                f"Error in request ... - status code = {response.status_code}",
                color="red",
                file=sys.stderr,
            )
            if response.status_code == 429:
                # delay = random.uniform(LONG_DELAY-5, LONG_DELAY+5)
                # time.sleep(delay)  # Wait before retrying
                retry_after = int(response.headers.get("Retry-After", 60))
                cprint(
                    f"Retry after {retry_after} secs ...",
                    "red",
                    file=sys.stderr,
                )
                time.sleep(retry_after)
            elif response.status_code == 403:
                # TODO with headers_403_bypass()
                if not bypassed_403:
                    cprint(
                        "403 Forbidden - Trying to bypass ...",
                        "yellow",
                        file=sys.stderr,
                    )
                    delay = random.uniform(
                        config["current_delay"] - 5, config["current_delay"] + 5
                    )
                    time.sleep(delay)  # Wait before retrying
                    response = start_request(
                        proxies=proxies,
                        base_url=base_url,
                        params=params,
                        headers=headers_403_bypass(),
                        secured=secured,
                        GET=GET,
                        config=config,
                        bypassed_403=True,
                    )
                else:
                    cprint(
                        "WAF is dropping suspicious requests. Scanning will continue after 10 minutes.",
                        color="red",
                        file=sys.stderr,
                    )
                    time.sleep(config["waf_delay"])
            else:
                cprint(
                    f"Error in request ... - status code = {response.status_code}",
                    color="red",
                    file=sys.stderr,
                )
                delay = random.uniform(
                    config["current_delay"] - 5, config["current_delay"] + 5
                )
                time.sleep(delay)  # Wait before retrying
            return response
        elif (
            "did not match any documents" in response.text
            and "Your search -" in response.text
        ):
            cprint(
                f"No results found for {params['q'] if  params and 'q' in params else params} with proxy {proxies}",
                "yellow",
                file=sys.stderr,
            )
            delay = random.uniform(
                config["current_delay"] - 5, config["current_delay"] + 5
            )
            time.sleep(delay)  # Wait before retrying
            return response
        # Placeholder for URL extraction logic
        cprint("Request successful - 200", "green", file=sys.stderr)
        delay = random.uniform(config["current_delay"] - 5, config["current_delay"] + 5)
        time.sleep(delay)  # Wait before retrying
        return response  # Return the category and a placeholder result
    except requests.exceptions.ProxyError as e:
        cprint(
            f"ProxyError searching for {params['q'] if  params and 'q' in params else params} with proxy {proxies}: {e}",
            "red",
            file=sys.stderr,
        )
        delay = random.uniform(config["current_delay"] - 2, config["current_delay"] + 2)
        time.sleep(delay)  # Wait before retrying
        return e.response
    except requests.exceptions.RequestException as e:
        cprint(
            f"RequestException searching for {params['q'] if  params and 'q' in params else params} with proxy {proxies}: {e}",
            "red",
            file=sys.stderr,
        )
        delay = random.uniform(config["current_delay"] - 2, config["current_delay"] + 2)
        time.sleep(delay)  # Wait before retrying
        return e.response
