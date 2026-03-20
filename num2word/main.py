"""CLI entry point — reads lines from a text file, converts numbers to words."""
import sys

from num2word.converter import convert
from num2word.extractor import extract_number


def process_line(line: str) -> str:
    number = extract_number(line)
    if number is None:
        return "number invalid"
    return convert(number)


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m num2word <input_file>", file=sys.stderr)
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


if __name__ == "__main__":
    main()
