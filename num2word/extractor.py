"""Extract and validate a number from a line of text."""
import re
from typing import Optional

# number must be standalone — not glued to special characters like #
STANDALONE_NUMBER = re.compile(r"(?:^|(?<=\s))(\d+)(?=\s|[.,;:!?]|$)")


def extract_number(line: str) -> Optional[int]:
    """Extract a single valid integer from a line, or None if invalid."""
    all_digits = re.findall(r"\d+", line)
    if len(all_digits) != 1:
        return None

    match = STANDALONE_NUMBER.search(line)
    if not match:
        return None

    return int(match.group(1))
