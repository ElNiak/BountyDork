#########################################################################################
# Google Dorking and searching functions
#########################################################################################

# Proxy-aware Google search function
import glob
import random
import threading
import time
import requests
from tqdm import tqdm
import sys
import re
import concurrent.futures
from termcolor import cprint

from utils.app_config import (
    USER_AGENTS,
)

from scraping.web_scraper import parse_google_search_results, render_js_and_get_text

from vpn_proxies.proxies_manager import get_proxies_and_cycle, prepare_proxies
from requester.request_manager import param_converter, start_request
from reporting.results_manager import (
    get_processed_dorks,
    save_dorking_query,
    google_dorking_results,
)

dork_id_lock = threading.Lock()


def google_search_with_proxy(
    dork_query,
    proxy,
    category,
    config,
    domain,
    processed_dorks,
    retries=1,
    advanced=False,
    dork_id=0,
):
    """Performs a Google search using a proxy.

    This function takes in various parameters to perform a Google search using a proxy.
    It generates a full query based on the provided dork query, config, and domain.
    It prepares the necessary parameters and proxies, and then performs the search using the `perform_searches` function.

    Args:
        dork_query (str): The dork query to be used for the Google search.
        proxy (str): The proxy to be used for the Google search.
        category (str): The category of the search.
        config (dict): The configuration file.
        domain (str): The domain to be searched.
        processed_dorks (list): A list of processed dorks.
        retries (int, optional): The number of retries for the search. Defaults to 1.
        advanced (bool, optional): Whether to use advanced search options. Defaults to False.
        dork_id (int, optional): The ID of the dork. Defaults to 0.

    Raises:
        Exception: If the config file is not provided.

    Returns:
        dict: The search results.
    """

    if not config:
        raise Exception("Config file should be provided")

    proxies = prepare_proxies(proxy, config)

    full_query = generate_dork_query(dork_query, config, domain)

    params = prepare_params(config)

    return perform_searches(
        full_query,
        proxies,
        category,
        params,
        retries,
        config,
        advanced,
        dork_id,
        processed_dorks,
        use_session=not (proxy == None),
    )


def prepare_params(config):
    return {
        "client": "ubuntu-sn",
        "channel": "fs",
        "num": config["total_output"],
        "hl": config["lang"],
    }


def perform_searches(
    full_query,
    proxies,
    category,
    params,
    retries,
    config,
    advanced,
    dork_id,
    processed_dorks,
    use_session,
):
    """Perform searches using Google dorking.

    This function performs searches using Google dorking technique. It takes various parameters
    to customize the search query and behavior.

    Args:
        full_query (str): The full search query.
        proxies (dict): A dictionary of proxies to be used for the search.
        category (str): The category of the search.
        params (dict): Additional parameters for the search.
        retries (int): The number of retries in case of failure.
        config (dict): Configuration settings for the search.
        advanced (bool): Flag indicating whether to use advanced search techniques.
        dork_id (int): The ID of the dork.
        processed_dorks (list): A list of processed dorks.
        use_session (bool): Flag indicating whether to use session for the search.

    Returns:
        int: The ID of the executed search.
    """

    params["q"] = full_query
    dork_id = execute_search_with_retries(
        full_query,
        proxies,
        category,
        params,
        retries,
        config,
        advanced,
        dork_id,
        processed_dorks,
        use_session=use_session,
    )

    return dork_id


def execute_search_with_retries(
    query,
    proxies,
    category,
    params,
    retries,
    config,
    advanced,
    dork_id,
    processed_dorks,
    use_session=False,
):
    """
    Execute a search with retries using Google dorking.

    Args:
        query (str): The search query.
        proxies (dict): The proxies to be used for the request.
        category (str): The category of the search.
        params (dict): The parameters for the request.
        retries (int): The number of retries.
        config (dict): The configuration settings.
        advanced (bool): Whether to use advanced search techniques.
        dork_id (int): The ID of the dork.
        processed_dorks (list): The list of already processed dorks.
        use_session (bool, optional): Whether to use a session for the request. Defaults to False.

    Returns:
        int: The updated dork ID.
    """
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip,deflate",
        "Connection": "close",
        "DNT": "1",
        "cache-control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
    }

    if query in processed_dorks:
        cprint(
            f"Skipping already processed dork: {query}",
            "yellow",
            file=sys.stderr,
        )
        return dork_id

    for retry_no in range(retries):
        if use_session:
            cprint(
                f"Searching for GET - Session (n° {retry_no}): {base_url} \n\t - parameters {params} \n\t - headers {headers} \n\t - {category} - with proxy {proxies} ...",
                "yellow",
                file=sys.stderr,
            )
            with requests.Session() as session:
                response = start_request(
                    config=config,
                    proxies=proxies,
                    base_url=base_url,
                    GET=True,
                    headers=headers,
                    params=params,
                    is_json=False,
                    secured=(
                        True
                        if proxies
                        and "https" in proxies
                        and proxies["https"]
                        and "socks" in proxies["https"]
                        else False
                    ),
                    session=session,
                    cookies={
                        "CONSENT": "PENDING+987",
                        "SOCS": "CAESHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiAo_CmBg",
                    },
                )
        else:
            cprint(
                f"Searching for GET (n° {retry_no}): {base_url} \n\t - parameters {params} \n\t - headers {headers} \n\t - {category} - with proxy {proxies} ...",
                "yellow",
                file=sys.stderr,
            )
            response = start_request(
                config=config,
                proxies=proxies,
                base_url=base_url,
                GET=True,
                headers=headers,
                params=params,
                is_json=False,
                secured=(
                    True
                    if proxies
                    and "https" in proxies
                    and proxies["https"]
                    and "socks" in proxies["https"]
                    else False
                ),
                cookies={
                    "CONSENT": "PENDING+987",
                    "SOCS": "CAESHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiAo_CmBg",
                },
            )

        urls = []
        if response:
            urls = parse_google_search_results(proxies, advanced, query, response.text)
            if (not urls or len(urls) == 0) and config["use_selenium"]:
                cprint(
                    f"Parsing for google search failed for {query} - retrying with selenium...",
                    "red",
                    file=sys.stderr,
                )
                html_content = render_js_and_get_text(
                    param_converter(params, url=base_url)
                )
                urls = parse_google_search_results(
                    proxies, advanced, query, html_content
                )
        result = dork_id, category, urls, query
        # save_dorking_query(result, config)
        with dork_id_lock:
            google_dorking_results.append((result, config))
        # with dork_id_lock:
        #     dork_id += 1
    # TODO to be faster also record non functionnal dork
    return dork_id


google_dork_tags = [
    "site:",  # Search within a specific site or domain
    "intitle:",  # Search for pages with a specific word in the title
    "inurl:",  # Search for pages with a specific word in the URL
    "intext:",  # Search for pages with a specific word in the text
    "filetype:",  # Search for files of a specific type (e.g., PDF, DOC)
    "ext:",  # Similar to filetype:, search for files with a specific extension
    "link:",  # Search for pages that link to a specific URL
    "cache:",  # Display Google's cached version of a page
    "related:",  # Find sites related to a given URL
    "info:",  # Show information about a specific URL
    "define:",  # Provide definitions for words
    "insubject:",  # Search for pages with a specific word in the subject (used in Google Groups)
    "daterange:",  # Search within a specific date range (using Julian dates)
    "allintitle:",  # Search for pages with all specified words in the title
    "allinurl:",  # Search for pages with all specified words in the URL
    "allintext:",  # Search for pages with all specified words in the text
    "allinanchor:",  # Search for pages with all specified words in the anchor text
    "author:",  # Search for articles written by a specific author (used in Google Groups)
    "group:",  # Search within a specific Google Group (used in Google Groups)
    "numrange:",  # Search within a specific number range
    "movie:",  # Search for information about a specific movie
    "map:",  # Search for maps
    "weather:",  # Get weather information
    "stocks:",  # Get stock information
    "phonebook:",  # Search for phonebook listings
    "book:",  # Search for books
    "safesearch:",  # Enable or disable safe search
    "blogurl:",  # Search for blogs at a specific URL
    "location:",  # Search for pages related to a specific location
    "before:",  # Search for pages before a specific date
    "after:",  # Search for pages after a specific date
]


def generate_dork_query(query, config, domain):
    """Generate a dork query for Google dorking.

    This function takes a query, configuration, and domain as input and generates a dork query
    for Google dorking. It cleans up the query by removing existing inurl: and intext: tags,
    ensures the query is properly enclosed in quotes if it contains quotes, and incorporates
    the subdomain into the search query if specified. It also appends the file extension to the
    query if specified in the configuration.

    Args:
        query (str): The query string.
        config (dict): The configuration settings.
        domain (str): The domain to incorporate into the search query.

    Returns:
        str: The generated dork query.

    """
    # Clean up the query by removing existing inurl: and intext: tags
    if len(query) > 0:
        for tag in ["inurl:", "intext:"]:
            query = query.replace(tag, "")

        # Ensure the query is properly enclosed in quotes if it contains quotes
        # if '"' in query:
        if not query.startswith('"'):
            query = '"' + query
        if not query.endswith('"'):
            query = query + '"'

        in_url_query = "inurl:" + query
        in_text_query = "intext:" + query

        query = in_url_query + " | " + in_text_query

        query = query  # + " | "  # + "inurl:&"

    # Incorporate subdomain into the search query if specified
    if domain:
        # Remove any existing site: tag and its value
        full_query = []
        query = re.sub(r"site:[^\s]+", "", query)
        to_search = f"site:{domain}"
        if len(query) > 0:
            full_query = f"({to_search}) & ({query})".strip()
        else:
            full_query = f"({to_search})".strip()
    else:
        full_query = f"({query})".strip()

    if config["extension"] and len(config["extension"]) > 0:
        full_query = full_query + f" & filetype:{config['extension']}"

    return full_query  # Indicate failure after retries


def filter_search_tasks(search_tasks, processed_dorks):
    """
    Filters out the already processed dorks from search tasks.

    Args:
        search_tasks (dict): A dictionary containing search tasks categorized by their respective categories.
        processed_dorks (list): A list of already processed dorks.

    Returns:
        dict: A dictionary containing filtered search tasks with the already processed dorks removed.

    """
    filtered_tasks = {}
    for category, dorks in search_tasks.items():
        filtered_tasks[category] = [
            dork for dork in dorks if dork not in processed_dorks
        ]
    return filtered_tasks


def launch_google_dorks_and_search_attack(config, categories):
    """Launches a Google dorks and search attack.

    This function takes a configuration object and a list of categories as input.
    It performs a Google dorks search for each category and launches a search attack
    using the obtained dorks.

    Args:
        config (dict): A configuration object containing various settings for the attack.
        categories (list): A list of categories to perform the search attack on.

    Raises:
        NotImplementedError: If VPN is enabled in the configuration, as VPN is not supported in this version.
        Exception: If any other error occurs during the search attack.

    Returns:
        None
    """
    start_time = time.time()
    try:

        proxies, proxy_cycle = get_proxies_and_cycle(config)

        search_tasks = {}

        for category in categories:
            search_tasks[category] = []
            dork_files = glob.glob(
                f"dorks/google/{category}/*.txt", recursive=True
            )
            for dork_file in dork_files:
                with open(dork_file, "r") as file:
                    lines = file.readlines()
                    dorks = [line.strip() for line in lines]
                search_tasks[category] += dorks

        cprint(
            f"Total number of dorks: {sum([len(search_tasks[task]) for task in search_tasks])}",
            "yellow",
            file=sys.stderr,
        )
        processed_dorks = get_processed_dorks(config)

        if not search_tasks:
            cprint(f"No dorks to process.", "red", file=sys.stderr)
            return

        if config["use_vpn"]:
            raise NotImplementedError(
                "VPN is not supported in this version - Error in library"
            )
            thread = threading.Thread(target=change_vpn)
            thread.start()

        number_of_worker = 30 # min(len(proxies)*2, 30)
        cprint(f"Number of workers: {number_of_worker}", "yellow", file=sys.stderr)

        search_tasks_with_proxy = []
        for task in search_tasks:
            for domain in config["subdomain"]:
                for dork in search_tasks[task]:
                    proxy = next(proxy_cycle)
                    search_tasks_with_proxy.append(
                        {
                            "dork": dork,
                            "proxy": proxy,
                            "category": task,
                            "domain": domain,
                        }
                    )
        cprint(
            f"Total number of dorks: {len(search_tasks_with_proxy)}",
            "yellow",
            file=sys.stderr,
        )
        # TODO https://stackoverflow.com/questions/65832061/threadpoolexecutor-keyboardinterrupt
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=number_of_worker
        ) as executor:
            future_to_search = {
                executor.submit(
                    google_search_with_proxy,
                    task["dork"],
                    task["proxy"],
                    task["category"],
                    config,
                    task["domain"],
                    processed_dorks,
                ): task
                for task in search_tasks_with_proxy
            }
            try:
                for future in tqdm(
                    concurrent.futures.as_completed(future_to_search),
                    total=len(future_to_search),
                    desc="Searching for vulnerable website",
                    unit="site",
                ):
                    future.result()
            except KeyboardInterrupt:
                cprint(
                    "Process interrupted by user during google dorking phase ... Saving results",
                    "red",
                    file=sys.stderr,
                )

                end_time = time.time()
                cprint(
                    "Total time taken: " + str(end_time - start_time), "green", file=sys.stderr
                )
                executor._threads.clear()
                concurrent.futures.thread._threads_queues.clear()
                # https://stackoverflow.com/questions/49992329/the-workers-in-threadpoolexecutor-is-not-really-daemon
                for result, config in google_dorking_results:
                    save_dorking_query(result, config)
                exit()

        end_time = time.time()
        cprint(
            "Total time taken: " + str(end_time - start_time), "green", file=sys.stderr
        )

        cprint(
            f"Saving dorks - Total number of dorks processed: {len(google_dorking_results)}",
            "green",
            file=sys.stderr,
        )

        # TODO remove duplicate url and merge dorks
        for result, config in google_dorking_results:
            save_dorking_query(result, config)
    except Exception as e:
        cprint(f"Error searching for dorks: {e}", "red", file=sys.stderr)
        raise e
