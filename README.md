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
    - Automate Google dorking
- **No need of API**: No need for API keys.
- **Reporting**: Generate detailed reports of findings.
- **Selenium**: Automate the process of finding vulnerabilities.
- **reCAPTCHA**: Automatically solve reCAPTCHA challenges.
- **VPN/Proxies Management**: Seamlessly switch between different VPN services and proxies to anonymize your activities.
- **Pause/Resume**: Pause and resume the dorking process at any time.

### Congiguration files

- **configs/config.ini**: Contains the configuration settings for the tool.


```ini
[Settings]
extension = 
subdomain = true
do_web_scap = true
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
