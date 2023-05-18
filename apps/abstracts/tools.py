from typing import Optional


def conver_to_int_or_none(number: str = "") -> Optional[int]:
    """Get converted string to number. If problem then None."""
    try:
        return int(number)
    except ValueError:
        return None
