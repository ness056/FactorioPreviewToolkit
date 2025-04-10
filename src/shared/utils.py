import re


def is_valid_map_string(s: str) -> bool:
    return bool(re.match(r"^>>>eN[a-zA-Z0-9+/=]+<<<$", s.strip()))
