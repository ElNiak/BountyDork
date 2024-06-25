import os
import sys
import time
from termcolor import cprint
import terminal_banner

#########################################################################################
# Animation
#########################################################################################

banner_res = """
        ___               ____
/ _ \___ ___ __ __/ / /____
/ , _/ -_|_-</ // / / __(_-<
/_/|_|\__/___/\_,_/_/\__/___/
*****************************

        """
banner_terminal_res = terminal_banner.Banner(banner_res)


def load_animation():
    banner = """

 ▄▄▄▄    ▒█████   █    ██  ███▄    █ ▄▄▄█████▓▓██   ██▓   ▓█████▄  ▒█████   ██▀███   ██ ▄█▀
▓█████▄ ▒██▒  ██▒ ██  ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒ ▒██  ██▒   ▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒ ██▄█▒ 
▒██▒ ▄██▒██░  ██▒▓██  ▒██░▓██  ▀█ ██▒▒ ▓██░ ▒░  ▒██ ██░   ░██   █▌▒██░  ██▒▓██ ░▄█ ▒▓███▄░ 
▒██░█▀  ▒██   ██░▓▓█  ░██░▓██▒  ▐▌██▒░ ▓██▓ ░   ░ ▐██▓░   ░▓█▄   ▌▒██   ██░▒██▀▀█▄  ▓██ █▄ 
░▓█  ▀█▓░ ████▓▒░▒▒█████▓ ▒██░   ▓██░  ▒██▒ ░   ░ ██▒▓░   ░▒████▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ █▄
░▒▓███▀▒░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒   ▒ ░░      ██▒▒▒     ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▒ ▓▒
▒░▒   ░   ░ ▒ ▒░ ░░▒░ ░ ░ ░ ░░   ░ ▒░    ░     ▓██ ░▒░     ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒ ▒░
 ░    ░ ░ ░ ░ ▒   ░░░ ░ ░    ░   ░ ░   ░       ▒ ▒ ░░      ░ ░  ░ ░ ░ ░ ▒    ░░   ░ ░ ░░ ░ 
 ░          ░ ░     ░              ░           ░ ░           ░        ░ ░     ░     ░  ░   
      ░                                        ░ ░         ░                               

                                        Made with ❤️
                        For the Community, By the Community

                        ###################################
                                Made by ElNiak
                linkedin  - https://www.linkedin.com/in/christophe-crochet-5318a8182/
                        Github - https://github.com/elniak

        """
    banner_terminal = terminal_banner.Banner(banner)
    cprint(banner_terminal, "green", file=sys.stderr)

    load_str = "Preparing the Dorking Pentesting...."
    ls_len = len(load_str)

    animation = "|/-\\"
    anicount = 0
    counttime = 0
    i = 0
    while counttime != 100:
        time.sleep(0.040)
        load_str_list = list(load_str)
        x = ord(load_str_list[i])
        y = 0
        if x != 32 and x != 46:
            if x > 90:
                y = x - 32
            else:
                y = x + 32
            load_str_list[i] = chr(y)

        res = ""
        for j in range(ls_len):
            res = res + load_str_list[j]

        sys.stdout.write("\r" + res + animation[anicount])
        sys.stdout.flush()

        load_str = res

        anicount = (anicount + 1) % 4
        i = (i + 1) % ls_len
        counttime = counttime + 1

    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")
