<h1 align="center">BountyDork</h1>
<p align="center">Bug Orientation tool Utilizing Novel Tactics Yields Dorking Research Implementing Vulnerability Exploitation </p><br>
<div align="center">
<img src="https://forthebadge.com/images/badges/made-with-python.svg" >
</div>

## Introduction:

BountyDork is a comprehensive tool designed for penetration testers and cybersecurity researchers. It integrates various modules for performing attacks, reporting, and managing VPN/proxy settings, making it an indispensable asset for any security professional.


## Features:
- **Automation**: Automate the process of finding vulnerabilities.
- **Dorking**:  
    - Automate Google dorking - `bounty_dork/dorks/google/<dorks>.txt`
- **No need of API**: No need for API keys.
- **Reporting**: Generate detailed reports of findings.
- **Selenium**: Automate the process of finding vulnerabilities.
- **reCAPTCHA**: Automatically solve reCAPTCHA challenges.
- **VPN/Proxies Management**: Seamlessly switch between different VPN services and proxies to anonymize your activities.
    
    - NordVPN - Create file `bounty_dork/vpn_proxies/proxies/nordvpn_login.csv` with `username,password` format.

```csv
username,password
AAAAAAAA,BBBBBBBB
```

- **Pause/Resume**: Pause and resume the dorking process at any time.
- **Pypy3 Support**: Use pypy3 to speed up the execution of the tool.

### Congiguration files

- **`configs/<hackerone>_targets.txt`**: Contains the list of targets to be scanned.

- **`configs/<hackerone>_exclusions.txt`**: Contains the list of exclusions to be used during scanning.

- **`outputs/reports/<hackerone>/*`**: Contains the list of outputs dorks to be used during scanning.

- **`configs/config.ini`**: Contains the configuration settings for the tool.

```ini
[Settings]
extension = 
subdomain = true
do_web_scap = true
dorks = bounty_dork/dorks/google/ ; TODO enforce
target_file = configs/target_toolsforhumanity.txt
exclusion_file = configs/exclusion_pornbox.txt
target_login = []
logging=DEBUG
max_thread = 30
runtime_save = true
keyboard_interrupt_save = true

[Bounty]
need_specific_user_agent = false
target_user_agent = RingResearcher_elniak
hackerone_username = elniak

[GoogleDorking]
do_dorking_google = true
total_output = 100
page_no = 1
default_total_output = 10
default_page_no = 1
lang = en
use_selenium = false
do_xss = true        ; enable xss dorking
do_sqli = true       ; enable sqli dorking


[GithubDorking]
do_dorking_github = false

[ShodanDorking]
do_dorking_shodan = false

[Proxy]
use_proxy = true
use_free_proxy_file = false
use_free_proxy = false
use_nordvpn_proxy = true
proxies = [None]
proxy_mean_delay = 10
proxy_factor = 1

[VPN]
use_vpn = false
use_nordvpn = false
nord_vpn_login = []

[Tor]
use_tor=false

[Delay]
initial_delay = 30
delay_factor = 2
long_delay = 15
max_delay = 600
request_delay = 30
waf_delay = 600

[Rate]
rate_per_minute = 1
current_delay = 60
```


## TODOs:

- **Logging Levels**: Implement logging level for the tool.

- **Dorking**:  
    - Automate Yahoo dorking
    - Automate Bing dorking
    - Automate DuckDuckGo dorking
    - Automate Ask dorking
    - Automate GitHub dorking
    - Automate Shodan dorking

- **Tor**:  
    - Automate Tor connection
    - Automate Tor disconnection

## Usage:

```bash
usage: bounty_dork.py [-h] --config CONFIG [--extension EXTENSION] [--subdomain SUBDOMAIN] [--do_web_scap DO_WEB_SCAP] [--target_file TARGET_FILE] [--exclusion_file EXCLUSION_FILE] [--target_login [TARGET_LOGIN ...]]
                      [--logging LOGGING] [--max_thread MAX_THREAD] [--runtime_save RUNTIME_SAVE] [--keyboard_interrupt_save KEYBOARD_INTERRUPT_SAVE] [--need_specific_user_agent NEED_SPECIFIC_USER_AGENT]
                      [--target_user_agent TARGET_USER_AGENT] [--hackerone_username HACKERONE_USERNAME] [--do_dorking_google DO_DORKING_GOOGLE] [--total_output TOTAL_OUTPUT] [--page_no PAGE_NO]
                      [--default_total_output DEFAULT_TOTAL_OUTPUT] [--default_page_no DEFAULT_PAGE_NO] [--lang LANG] [--use_selenium USE_SELENIUM] [--do_dorking_github DO_DORKING_GITHUB] [--do_dorking_shodan DO_DORKING_SHODAN]
                      [--use_proxy USE_PROXY] [--use_free_proxy_file USE_FREE_PROXY_FILE] [--use_free_proxy USE_FREE_PROXY] [--use_nordvpn_proxy USE_NORDVPN_PROXY] [--proxies [PROXIES ...]] [--proxy_mean_delay PROXY_MEAN_DELAY]
                      [--proxy_factor PROXY_FACTOR] [--use_vpn USE_VPN] [--use_nordvpn USE_NORDVPN] [--nord_vpn_login [NORD_VPN_LOGIN ...]] [--use_tor USE_TOR] [--initial_delay INITIAL_DELAY] [--delay_factor DELAY_FACTOR]
                      [--long_delay LONG_DELAY] [--max_delay MAX_DELAY] [--request_delay REQUEST_DELAY] [--waf_delay WAF_DELAY] [--rate_per_minute RATE_PER_MINUTE] [--current_delay CURRENT_DELAY]

Configuration and Argument Parser

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the configuration file
  --extension EXTENSION
                        Extension
  --subdomain SUBDOMAIN
                        Use subdomain
  --do_web_scap DO_WEB_SCAP
                        Do web scraping
  --target_file TARGET_FILE
                        Target file
  --exclusion_file EXCLUSION_FILE
                        Exclusion file
  --target_login [TARGET_LOGIN ...]
                        Target login
  --logging LOGGING     Logging level
  --max_thread MAX_THREAD
                        Maximum number of threads
  --runtime_save RUNTIME_SAVE
                        Runtime save
  --keyboard_interrupt_save KEYBOARD_INTERRUPT_SAVE
                        Keyboard interrupt save
  --need_specific_user_agent NEED_SPECIFIC_USER_AGENT
                        Need specific user agent
  --target_user_agent TARGET_USER_AGENT
                        Target user agent
  --hackerone_username HACKERONE_USERNAME
                        HackerOne username
  --do_dorking_google DO_DORKING_GOOGLE
                        Do Google dorking
  --total_output TOTAL_OUTPUT
                        Total output
  --page_no PAGE_NO     Page number
  --default_total_output DEFAULT_TOTAL_OUTPUT
                        Default total output
  --default_page_no DEFAULT_PAGE_NO
                        Default page number
  --lang LANG           Language
  --use_selenium USE_SELENIUM
                        Use Selenium
  --do_dorking_github DO_DORKING_GITHUB
                        Do GitHub dorking
  --do_dorking_shodan DO_DORKING_SHODAN
                        Do Shodan dorking
  --use_proxy USE_PROXY
                        Use proxy
  --use_free_proxy_file USE_FREE_PROXY_FILE
                        Use free proxy file
  --use_free_proxy USE_FREE_PROXY
                        Use free proxy
  --use_nordvpn_proxy USE_NORDVPN_PROXY
                        Use NordVPN proxy
  --proxies [PROXIES ...]
                        Proxies
  --proxy_mean_delay PROXY_MEAN_DELAY
                        Proxy mean delay
  --proxy_factor PROXY_FACTOR
                        Proxy factor
  --use_vpn USE_VPN     Use VPN
  --use_nordvpn USE_NORDVPN
                        Use NordVPN
  --nord_vpn_login [NORD_VPN_LOGIN ...]
                        NordVPN login
  --use_tor USE_TOR     Use Tor
  --initial_delay INITIAL_DELAY
                        Initial delay
  --delay_factor DELAY_FACTOR
                        Delay factor
  --long_delay LONG_DELAY
                        Long delay
  --max_delay MAX_DELAY
                        Max delay
  --request_delay REQUEST_DELAY
                        Request delay
  --waf_delay WAF_DELAY
                        WAF delay
  --rate_per_minute RATE_PER_MINUTE
                        Rate per minute
  --current_delay CURRENT_DELAY
                        Current delay

```

OR


```bash
python3 bounty_dork.py --config <config_file>

-Extension: 
-Total Output: 100
-Page No: 1
-Do Google Dorking: True
-Do Github Dorking False
-Domain: True
-Use Proxy: True

Using NordVPN proxies 
You have NordVPN account using these proxies [['AAAA', 'BBBB']]
NordVPN Proxy: amsterdam.nl.socks.nordhold.net
NordVPN Proxy: atlanta.us.socks.nordhold.net
NordVPN Proxy: dallas.us.socks.nordhold.net
NordVPN Proxy: los-angeles.us.socks.nordhold.net
NordVPN Proxy: nl.socks.nordhold.net
NordVPN Proxy: se.socks.nordhold.net
NordVPN Proxy: stockholm.se.socks.nordhold.net
NordVPN Proxy: us.socks.nordhold.net
NordVPN Proxy: new-york.us.socks.nordhold.net

Proxy: ['socks5h://username:password@los-angeles.us.socks.nordhold.net:1080', 'socks5h://username:password@us.socks.nordhold.net:1080', 'socks5h://username:password@new-york.us.socks.nordhold.net:1080', 'socks5h://username:password@amsterdam.nl.socks.nordhold.net:1080', 'socks5h://username:password@dallas.us.socks.nordhold.net:1080', 'socks5h://username:password@atlanta.us.socks.nordhold.net:1080', 'socks5h://username:password@nl.socks.nordhold.net:1080', 'socks5h://username:password@stockholm.se.socks.nordhold.net:1080', 'socks5h://username:password@se.socks.nordhold.net:1080']

Number of workers: 30

Starting Google dorking scan phase...

Initial Dorking search for based targets *.worldcoin.org - xss
Initial Dorking search for based targets *.worldcoin.org - sqli
Initial Dorking search for based targets *.consumer.worldcoin.org - xss
Initial Dorking search for based targets *.consumer.worldcoin.org - sqli
Initial Dorking search for based targets toolsforhumanity.com - xss
Initial Dorking search for based targets toolsforhumanity.com - sqli
Initial Dorking search for based targets getworldcoin.com - xss
Initial Dorking search for based targets getworldcoin.com - sqli
Initial Dorking search for based targets *.worldcoin-distributors.com - xss
Initial Dorking search for based targets *.worldcoin-distributors.com - sqli
Initial Dorking search for based targets bioid-management.app - xss
Initial Dorking search for based targets bioid-management.app - sqli
Initial Dorking search for based targets *.worldcoin.dev - xss
Initial Dorking search for based targets *.worldcoin.dev - sqli
Initial Dorking search for based targets worldcoin.org - xss
Initial Dorking search for based targets worldcoin.org - sqli
Initial Dorking search for based targets *.toolsforhumanity.com - xss
Initial Dorking search for based targets *.toolsforhumanity.com - sqli
Initial Dorking search for based targets support.worldcoin.com - xss
Initial Dorking search for based targets support.worldcoin.com - sqli
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.worldcoin.org)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@dallas.us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.worldcoin.org)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@amsterdam.nl.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.consumer.worldcoin.org)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@stockholm.se.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:toolsforhumanity.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@atlanta.us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:toolsforhumanity.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; en-us; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:getworldcoin.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 13729.56.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@new-york.us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.consumer.worldcoin.org)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@nl.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:getworldcoin.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@se.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:bioid-management.app)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@amsterdam.nl.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.worldcoin-distributors.com)'} 
	 - headers {'User-Agent': 'Wget/1.15 (linux-gnu)', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@dallas.us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.worldcoin.dev)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@nl.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.worldcoin.dev)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@atlanta.us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:worldcoin.org)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 13729.56.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.toolsforhumanity.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@se.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.toolsforhumanity.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@los-angeles.us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:support.worldcoin.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@dallas.us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:*.worldcoin-distributors.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - xss - with proxy {'https': 'socks5h://AAAAA:BBBB@los-angeles.us.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:bioid-management.app)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 13729.56.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@stockholm.se.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:support.worldcoin.com)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@amsterdam.nl.socks.nordhold.net:1080'} ...
Searching for GET - Session (n° 0): https://www.google.com/search 
	 - parameters {'client': 'ubuntu-sn', 'channel': 'fs', 'num': 10, 'hl': 'en', 'q': '(site:worldcoin.org)'} 
	 - headers {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip,deflate', 'Connection': 'close', 'DNT': '1', 'cache-control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} 
	 - sqli - with proxy {'https': 'socks5h://AAAAA:BBBB@new-york.us.socks.nordhold.net:1080'} ...
Initializing Dorking of targets:   0%|          | 0/20 [00:00<?, ?site/s]Request successful - 200
Request successful - 200
Request successful - 200
Request successful - 200
Request successful - 200
No results found for (site:*.consumer.worldcoin.org) with proxy {'https': 'socks5h://AAAAA:BBBB@nl.socks.nordhold.net:1080'}
Request successful - 200
No results found for (site:*.consumer.worldcoin.org) with proxy {'https': 'socks5h://AAAAA:BBBB@stockholm.se.socks.nordhold.net:1080'}
Request successful - 200
Request successful - 200
Request successful - 200
Request successful - 200
No results found for (site:*.worldcoin-distributors.com) with proxy {'https': 'socks5h://AAAAA:BBBB@dallas.us.socks.nordhold.net:1080'}
Request successful - 200
Request successful - 200
Request successful - 200
Request successful - 200
Request successful - 200
No results found for (site:*.worldcoin-distributors.com) with proxy {'https': 'socks5h://AAAAA:BBBB@los-angeles.us.socks.nordhold.net:1080'}
Request successful - 200



```

## Python

- **Python3** is natively supported:
    
```bash
# Dorking process time with 9 threads:

  

```

- **pypy3 Support**: Use pypy3 to speed up the execution of the tool:

```bash
# Dorking process time with 9 threads:



```

## Installation:

### Packages:

```bash
# For reCAPTCHA
sudo apt-get install portaudio19-dev

```

### Pre-Commit:

```bash
python3 -m pip install pre-commit
pre-commit installed at .git/hooks/pre-commit
mypy bounty_drive/
```

### Classical:

```bash
sudo apt-get install python3 python3-dev python3-venv
python3 --version
# Python 3.10.12
```

```bash
python3 -m venv python3-venv
source python3-venv/bin/activate
python3 -m pip install -U pip wheel
python3 -m pip install -r requirements.txt
```

Update `config.ini`

Run with `python3 bounty_dork.py`
