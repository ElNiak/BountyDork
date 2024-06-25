import sys
from termcolor import cprint
from vpn_proxies.nordvpn_switcher.nordvpn_switch import (
    initialize_VPN,
    rotate_VPN,
    terminate_VPN,
)


def setup_vpn(config):
    """Set up VPN based on the provided configuration.

    Args:
        config (dict): A dictionary containing the VPN configuration.

    Raises:
        NotImplementedError: Raised if NordVPN is not supported in this version.
    """
    if config["use_nordvpn"]:
        raise NotImplementedError(
            "NordVPN is not supported in this version - Error in library"
        )
        if len(config["nord_vpn_login"]) > 0:
            try:
                initialize_VPN(save=1, area_input=["complete rotation"])
            except Exception as e:
                cprint(
                    f"VPN initialization error: {e}",
                    "red",
                    file=sys.stderr,
                )
                config["use_nordvpn"] = False
        else:
            cprint(
                "You need to provide NordVPN credentials to use VPN",
                "red",
                file=sys.stderr,
            )
            config["use_nordvpn"] = False


def change_vpn(time=300):
    rotate_VPN()
    time.sleep(time)
