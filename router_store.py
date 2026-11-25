import json
import ipaddress
from pathlib import Path

# Location of our JSON storage file
DATA_FILE = Path(__file__).parent / "data" / "routers.json"


def load_routers():
    """Load saved router configurations from the JSON file."""
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r") as file:
            saved_data = json.load(file)

        routers = {}

        for device_name, config in saved_data.items():
            routers[device_name] = (
                config["ip"],
                config["port"]
            )

        return routers

    except (json.JSONDecodeError, KeyError, TypeError):
        return {}


def save_routers(routers):
    """Save router configurations to the JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    saved_data = {}

    for device_name, config in routers.items():
        saved_data[device_name] = {
            "ip": config[0],
            "port": config[1]
        }

    with open(DATA_FILE, "w") as file:
        json.dump(saved_data, file, indent=4)


# This dictionary stores all router configurations.
# Each value is a tuple: (IP address, port).
router_configs = load_routers()


def add_router(device_name, ip_address, port):
    """Add a router without overwriting an existing device."""

    device_name = device_name.strip()

    if not device_name:
        return False, "Device name cannot be empty."

    if device_name in router_configs:
        return False, "A router with this device name already exists."

    try:
        ipaddress.IPv4Address(ip_address)
    except ipaddress.AddressValueError:
        return False, "Please enter a valid IPv4 address."

    try:
        port = int(port)
    except (ValueError, TypeError):
        return False, "Port must be a number."

    if not 1 <= port <= 65535:
        return False, "Port must be between 1 and 65535."

    # Store IP and port together as an immutable tuple.
    router_configs[device_name] = (ip_address, port)

    save_routers(router_configs)

    return True, "Router added successfully."


def get_routers():
    """Return all saved router configurations."""
    return router_configs.copy()


def search_router(device_name):
    """Find a router using its device name."""
    return router_configs.get(device_name.strip())

def delete_router(device_name):
    """Delete a router using its device name."""

    device_name = device_name.strip()

    if device_name not in router_configs:
        return False, "Router not found."

    del router_configs[device_name]

    save_routers(router_configs)

    return True, "Router deleted successfully."