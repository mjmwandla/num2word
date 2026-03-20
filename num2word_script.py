"""Number to words converter — single script version.

Usage: python num2word_script.py input.txt
"""
import re
import sys
from typing import Optional

MAX_SUPPORTED = 999_999_999_999_999

# empty strings so index matches the number, teens are irregular so we store them directly
ONES = [
    "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen",
]

TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
]

# number must be standalone — not glued to special characters like #
STANDALONE_NUMBER = re.compile(r"(?:^|(?<=\s))(\d+)(?=\s|[.,;:!?]|$)")


def convert_below_hundred(n: int) -> str:
    """Convert 0-99 to words."""
    if n < 20:
        return ONES[n]
    tens_part = TENS[n // 10]
    ones_part = ONES[n % 10]
    return f"{tens_part}-{ones_part}" if ones_part else tens_part


def convert_below_thousand(n: int) -> str:
    """Convert 0-999 to words."""
    if n < 100:
        return convert_below_hundred(n)
    hundreds_digit = n // 100
    remainder = n % 100
    result = f"{ONES[hundreds_digit]} hundred"
    if remainder:
        result += f" and {convert_below_hundred(remainder)}"
    return result


def convert(n: int) -> str:
    """Convert a non-negative integer to English words."""
    if not isinstance(n, int):
        raise TypeError(f"expected int, got {type(n).__name__}")
    if n < 0:
        raise ValueError("negative numbers are not supported")
    if n > MAX_SUPPORTED:
        raise ValueError(f"number too large, max supported is {MAX_SUPPORTED}")
    if n == 0:
        return "zero"

    groups = []
    while n > 0:
        groups.append(n % 1000)
        n //= 1000

    SCALES = ["", "thousand", "million", "billion", "trillion"]

    parts = []
    for group, scale in zip(groups, SCALES):
        if group != 0:
            word = convert_below_thousand(group)
            parts.append(f"{word} {scale}".strip())

    parts.reverse()

    if len(parts) > 1 and 0 < groups[0] < 100:
        return ', '.join(parts[:-1]) + ' and ' + parts[-1]

    return ', '.join(parts)


def extract_number(line: str) -> Optional[int]:
    """Extract a single valid integer from a line, or None if invalid."""
    all_digits = re.findall(r"\d+", line)
    if len(all_digits) != 1:
        return None

    match = STANDALONE_NUMBER.search(line)
    if not match:
        return None

    return int(match.group(1))


def process_line(line: str) -> str:
    number = extract_number(line)
    if number is None:
        return "number invalid"
    return convert(number)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python num2word_script.py <input_file>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line:
                    print(process_line(line))
    except FileNotFoundError:
        print(f"Error: file '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
