import re

def is_valid_mac(mac: str) -> bool:
    """Checks if a MAC address is valid."""
    mac_regex = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return bool(re.match(mac_regex, mac))

def normalize_mac(mac: str) -> str:
    """Normalizes a MAC address to use colons and uppercase letters."""
    return mac.replace("-", ":").upper()