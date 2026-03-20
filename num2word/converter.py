"""Convert an integer to its English word representation."""

MAX_SUPPORTED = 999_999_999_999_999  # up to trillions

# empty strings so index matches the number, teens are irregular so we store them directly
ONES = [
    "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen",
]

TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
]


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
