import json
import os
import random
import re
import sys
import tempfile
import time
import unicodedata
from urllib.parse import urljoin
import uuid
import requests
import speech_recognition
from pydub import AudioSegment

# web_scraper.py
import requests
from bs4 import BeautifulSoup
from termcolor import cprint

from utils.app_config import USER_AGENTS

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    from selenium.webdriver.firefox.service import Service as FireFoxService
    from selenium.webdriver.firefox.options import Options as FireFoxOptions

    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException
except ImportError:
    cprint(
        "Selenium is not installed. Please install it using 'pip install selenium'.",
        "red",
        file=sys.stderr,
    )
    sys.exit(1)


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def you_are_human(response):
    """_summary_

    Args:
        response (_type_): _description_

    Returns:
        _type_: _description_
    """
    soup = BeautifulSoup(response, "html.parser")
    if soup.find("div", {"class": "g-recaptcha"}):
        # https://www.zenrows.com/blog/please-verify-you-are-human#headless-browser
        return True
    return False


# https://github.com/thicccat688/selenium-recaptcha-solver/blob/main/selenium_recaptcha_solver/solver.py#L153
def by_pass_captcha(driver):
    """_summary_

    Args:
        driver (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (
                    By.CSS_SELECTOR,
                    "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']",
                )
            )
        )
        time.sleep(random.uniform(2, 10))
        cprint("Click reCAPTCHA ...", color="yellow", file=sys.stderr)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))
        ).click()
        time.sleep(random.uniform(2, 10))
    except TimeoutException:
        cprint("reCAPTCHA not found ...", color="red", file=sys.stderr)
        return

    # If the captcha image audio is available, locate it. Otherwise, skip to the next line of code.
    try:
        cprint(
            "Bypassing reCAPTCHA - Audio phase - captcha image audio is available, locate it.",
            color="yellow",
            file=sys.stderr,
        )
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-audio-button"]'))
        ).click()
        time.sleep(random.uniform(2, 10))
    except TimeoutException:
        cprint(
            "Bypassing reCAPTCHA - Audio phase - captcha image audio is not available, skip to the next line of code.",
            color="yellow",
            file=sys.stderr,
        )
        pass

    try:
        bypass_captcha_audio_phase(driver)
        time.sleep(random.uniform(2, 10))
    except Exception as e:
        cprint(
            f"Error bypassing reCAPTCHA - Audio phase: {e}",
            color="red",
            file=sys.stderr,
        )
        return

    # Locate verify button and click it via JavaScript
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))
    ).click()
    time.sleep(random.uniform(2, 10))
    try:
        cprint(
            "Bypassing reCAPTCHA - Audio phase solve more",
            color="yellow",
            file=sys.stderr,
        )

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    '//div[normalize-space()="Multiple correct solutions required - please solve more."]',
                )
            )
        )
        time.sleep(random.uniform(2, 10))
        bypass_captcha_audio_phase(driver)
        time.sleep(random.uniform(2, 10))
        # Locate verify button again to avoid stale element reference and click it via JavaScript
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))
        ).click()
    except TimeoutException:
        cprint(
            "Bypassing reCAPTCHA - Audio phase - Multiple correct solutions required - please solve more.",
            color="yellow",
            file=sys.stderr,
        )
        pass

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def parse_headers(headers):
    headers = headers.replace('\\n', '\n')
    sorted_headers = {}
    matches = re.findall(r'(.*):\s(.*)', headers)
    for match in matches:
        header = match[0]
        value = match[1]
        try:
            if value[-1] == ',':
                value = value[:-1]
            sorted_headers[header] = value
        except IndexError:
            pass
    return sorted_headers

def bypass_captcha_audio_phase(driver):
    recognizer = speech_recognition.Recognizer()

    try:
        cprint(
            "Bypassing reCAPTCHA - Audio phase download",
            color="yellow",
            file=sys.stderr,
        )
        # Locate audio challenge download link
        # Get the audio challenge URI from the download link
        download_link = driver.find_element(
            By.XPATH, "rc-audiochallenge-tdownload-link"
        )
        cprint("Download link found", color="green", file=sys.stderr)

    except TimeoutException:
        raise Exception("Google has detected automated queries. Try again later.")
    except Exception as e:
        raise Exception(f"Error locating download link: {e}")

    # Create temporary directory and temporary files
    tmp_dir = tempfile.gettempdir()

    id_ = uuid.uuid4().hex

    mp3_file, wav_file = os.path.join(tmp_dir, f"{id_}_tmp.mp3"), os.path.join(
        tmp_dir, f"{id_}_tmp.wav"
    )
    cprint(
        f"Temporary files created: {mp3_file}, {wav_file}",
        color="yellow",
        file=sys.stderr,
    )
    tmp_files = {mp3_file, wav_file}

    with open(mp3_file, "wb") as f:
        link = download_link.get_attribute("href")

        audio_download = requests.get(url=link, allow_redirects=True)

        f.write(audio_download.content)

        f.close()

    # Convert MP3 to WAV format for compatibility with speech recognizer APIs
    AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")

    # Disable dynamic energy threshold to avoid failed reCAPTCHA audio transcription due to static noise
    recognizer.dynamic_energy_threshold = False

    with speech_recognition.AudioFile(wav_file) as source:
        audio = recognizer.listen(source)

        try:
            recognized_text = recognizer.recognize_google(audio, "en-US")

        except speech_recognition.UnknownValueError:
            raise Exception(
                "Speech recognition API could not understand audio, try again"
            )

    # Clean up all temporary files
    for path in tmp_files:
        if os.path.exists(path):
            os.remove(path)

    # Write transcribed text to iframe's input box
    response_textbox = driver.find_element(By.ID, "audio-response")

    for c in recognized_text:
        response_textbox.send_keys(c)
        time.sleep(random.uniform(0.05, 0.1))

    # # Switch to iframe that directly houses pX "Press & Hold" button
    # WebDriverWait(driver, timeout=300).until(
    #     EC.frame_to_be_available_and_switch_to_it("iframe_name_or_id")
    # )
    # # Get button element
    # btn = driver.find_element(By.XPATH, "//xpath_to_button")
    # # Initialize for low-level interactions
    # action = ActionChains(driver)
    # action.click_and_hold(btn)
    # # Initiate clich and hold action on button
    # action.perform()
    # # Keep holding for 10s
    # time.sleep(10)
    # # Release button
    # action.release(btn)


def parse_google_search_results(proxies, advanced, full_query, response):
    """_summary_

    Args:
        proxies (_type_): _description_
        advanced (_type_): _description_
        full_query (_type_): _description_
        response (_type_): _description_

    Returns:
        _type_: _description_
    """
    urls = []
    soup = BeautifulSoup(response, "html.parser")
    result_block = soup.find_all("div", attrs={"class": "g"})
    cprint(
        f"Potentially {len(result_block)} links ...",
        "yellow",
        file=sys.stderr,
    )
    if len(result_block) == 0:
        cprint(
            f"No results found for parsing of {full_query} with proxy {proxies}\nTrying new parsing method",
            "yellow",
            file=sys.stderr,
        )
        try:
            filename = "outputs/html_google_todo/" + slugify(f"google_search_{full_query}") + ".html"
            with open(
                filename, "w"
            ) as f:
                f.write(response)
        except Exception as e:
            cprint(
                f"Error writing to file: {e}",
                "red",
                file=sys.stderr,
            )
        # Locate all <a> tags that contain the search results
        for a_tag in soup.find_all("a", href=True):
            # Extract the href attribute
            href = a_tag["href"]
            # Only consider hrefs that start with '/url?'
            if href.startswith("/url?"):
                # Extract the actual URL using regex
                url_match = re.search(r"(https?://[^&]+)", href)
                if url_match:
                    url = url_match.group(0)
                    cprint(f"Checking for url: {url}", color="yellow", file=sys.stderr)
                    # Extract the title (text within <div> with specific class)
                    title_tag = a_tag.find("h3") or a_tag.find(
                        "div", class_="BNeawe vvjwJb AP7Wnd UwRFLe"
                    )
                    title = title_tag.get_text() if title_tag else None
                    if title:
                        cprint(
                            f"Link appended to potential urls: {url}",
                            "green",
                            file=sys.stderr,
                        )
                        urls.append(url)
            else:
                pass
    else:
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find("div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    cprint(
                        f"Link appended to potential urls: {link['href']}",
                        "green",
                        file=sys.stderr,
                    )
                    if advanced:
                        urls.append(SearchResult(link["href"], title.text, description))
                    else:
                        urls.append(link["href"])
    cprint(
        f"Done parsing search results - {len(urls)} potential new links",
        "green",
        file=sys.stderr,
    )
    return urls


def fetch_html_content(url, config, proxy=None, headers=None):
    """
    Fetch the HTML content of a given URL.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: HTML content of the page or None if request fails.
    """
    try:
        cprint(f"Fetching {url}", color="yellow", file=sys.stderr)
        if proxy and "username:password" in proxy:
            print(f"logins :{json.loads(config['nord_vpn_login'])}")
            nord_vpn_user_pass = random.choice(json.loads(config["nord_vpn_login"]))
            proxy = proxy.replace("username", nord_vpn_user_pass[0]).replace(
                "password", nord_vpn_user_pass[1]
            )
            proxies = {"https": proxy}
            secured = True
        else:
            proxies = {"http": proxy, "https": proxy}
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "X-HackerOne-Research": "elniak",
        }
        response = requests.Session().get(
            url,
            proxies=proxies,
            headers=headers,
            verify=secured,
            allow_redirects=True,
            timeout=config["request_delay"],
        )
        delay = random.uniform(config["current_delay"] - 5, config["current_delay"] + 5)
        time.sleep(delay)  # Wait before retrying
        return response.text
    except requests.exceptions.ProxyError as e:
        cprint(
            f"ProxyError searching for {url} with proxy {proxies}: {e}",
            "red",
            file=sys.stderr,
        )
        delay = random.uniform(config["current_delay"] - 2, config["current_delay"] + 2)
        time.sleep(delay)  # Wait before retrying
        # TODO add backoff timer for delay ?
        return None
    except requests.exceptions.RequestException as e:
        cprint(
            f"RequestException searching for {url} with proxy {proxies}: {e}",
            "red",
            file=sys.stderr,
        )
        delay = random.uniform(config["current_delay"] - 5, config["current_delay"] + 5)
        time.sleep(delay)  # Wait before retrying
        return None


def extract_links(html_content, base_url):
    """
    Extract all href links from the HTML content and convert to absolute URLs.

    Args:
        html_content (str): HTML content of the page.
        base_url (str): The base URL to resolve relative URLs.

    Returns:
        list: List of absolute URLs found in the href attributes and other redirections.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    links = []

    # Extracting href attributes from anchor tags
    for anchor in soup.find_all("a", href=True):
        link = urljoin(base_url, anchor["href"])
        links.append(link)

    # Extracting other potential redirections (meta refresh, script-based)
    for meta in soup.find_all("meta", attrs={"http-equiv": "refresh"}):
        content = meta.get("content", "")
        if "url=" in content:
            link = urljoin(base_url, content.split("url=")[-1])
            links.append(link)

    # Handle common JavaScript redirection patterns
    for script in soup.find_all("script"):
        if script.string:
            js_urls = re.findall(
                r"window\.location\.href\s*=\s*['\"](.*?)['\"]", script.string
            )
            for js_url in js_urls:
                link = urljoin(base_url, js_url)
                links.append(link)

    print(f"Extracted {len(links)} links from {base_url}", file=sys.stderr)
    return links


standard_monitors_size = [
    (1920, 1080),
    (1280, 720),
    (854, 480),
    (640, 360),
    (426, 240),
]


random_drivers = ["webdriver.Chrome", "webdriver.Firefox", "webdriver.Edge"]


def render_js_and_get_text(url, proxy=None):
    """
    Use Selenium to render JavaScript and extract links.

    Args:
        url (str): URL of the page to scrape.

    Returns:
        list: List of absolute URLs found in the rendered HTML.
    """
    cprint(f"Rendering JavaScript for {url}", color="yellow", file=sys.stderr)
    try:
        options = Options()
        options.headless = True

        # options.binary_location = "/snap/bin/firefox"
        size = random.choice(standard_monitors_size)
        cprint(f"Selenium Using Size - {size}", color="yellow", file=sys.stderr)
        options.add_argument(f"window-size={size[0]},{size[1]}")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        # service=Service('/path/to/chromedriver'),
        driver = webdriver.Chrome(options=options)  # TODO use edge driver
        # driver = webdriver.Firefox(options=options)

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
        }

        # Create a request interceptor
        def interceptor(request):
            request.headers = headers

        # Set the interceptor on the driver
        driver.request_interceptor = interceptor

        # driver.set_window_size(size[0],size[1])

        driver.get(url)

        by_pass_captcha(driver)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        html_content = driver.page_source
        driver.quit()
    except Exception as e:
        cprint(f"Error rendering JS for {url}: {e}", color="red", file=sys.stderr)
        # return []
        html_content = ""
    finally:
        return html_content


def render_js_and_extract_links(url, html_content_get, proxy=None):
    """
    Use Selenium to render JavaScript and extract links.

    Args:
        url (str): URL of the page to scrape.

    Returns:
        list: List of absolute URLs found in the rendered HTML.
    """
    cprint(f"Rendering JavaScript for {url}", color="yellow", file=sys.stderr)
    try:
        options = Options()
        options.headless = True
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        # service=Service('/path/to/chromedriver'),
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        html_content = driver.page_source
        driver.quit()
    except Exception as e:
        cprint(f"Error rendering JS for {url}: {e}", color="red", file=sys.stderr)
        # return []
        html_content = ""
    return extract_links(html_content, url) + extract_links(html_content_get, url)


def scrape_links_from_url(url, proxy=None, headers=None):
    """
    Scrape all potential links and redirections from a given URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        list: List of URLs found in the page.
    """

    cprint(f"Scraping links from {url}", color="yellow", file=sys.stderr)
    html_content = fetch_html_content(url, proxy=proxy, headers=headers)
    if html_content:
        return render_js_and_extract_links(url, html_content, proxy=proxy)
    return []
