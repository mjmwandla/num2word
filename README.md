# Number to Words Converter

[![tests](https://github.com/mjmwandla/num2word/actions/workflows/tests.yml/badge.svg)](https://github.com/mjmwandla/num2word/actions/workflows/tests.yml)

Extracts a number from a line of text and converts it to English words.

## How to Run

Python 3.6+, no external dependencies.

```bash
# package version
python3 -m num2word input.txt

# or single script version
python3 num2word_script.py input.txt

# run tests
python3 -m unittest discover tests -v
```

Optionally install as a CLI tool:
```bash
pip install .
num2word input.txt
```

## Example

Input (`input.txt`):
```
The pump is 536 deep underground.
We processed 9121 records.
Variables reported as having a missing type #65678.
Interactive and printable 10022 ZIP code.
The database has 66723107008 records.
I received 23 456,9 KGs.
```

Output:
```
five hundred and thirty-six
nine thousand, one hundred and twenty-one
number invalid
ten thousand and twenty-two
sixty-six billion, seven hundred and twenty-three million, one hundred and seven thousand and eight
number invalid
```

## Project Structure

```
num2word/
    __init__.py
    __main__.py          # enables `python -m num2word`
    converter.py         # number → English words
    extractor.py         # extract & validate number from text
    main.py              # CLI entry point
tests/
    test_converter.py    # unit tests for conversion
    test_extractor.py    # unit tests for extraction
    test_integration.py  # end-to-end pipeline tests
num2word_script.py       # single file version
num2word_solution.ipynb  # notebook version
pyproject.toml           # packaging config
input.txt
```

Extraction and conversion are separate modules because they're different problems — one is text parsing, the other is number formatting. Each can be tested and changed independently.

## Design Choices

**Lookup tables** — English number names are irregular (eleven, twelve, thirteen... not "oneteen"). The teens break any pattern, so a table for 0–19 is the only clean approach.

**Groups of three** — The converter breaks numbers into groups of 3 digits from right to left, pairs each group with a scale word (thousand, million, billion), then joins them. This mirrors how English actually speaks numbers.

**"And" placement** — "and" goes before the tens/ones portion within a group ("five hundred **and** thirty-six") and before the final group when it's below 100 ("ten thousand **and** twenty-two"). Between major groups, a comma is used ("nine thousand**,** one hundred and twenty-one").

**Validation rules** — Derived from the test cases:
- `#65678` → invalid: glued to `#`, it's an identifier not a number
- `23 456,9` → invalid: multiple digit sequences = ambiguous
- A valid number must be standalone (whitespace or punctuation on both sides)

**Input validation** — `convert()` raises `TypeError` for non-integers and `ValueError` for negatives or numbers beyond the supported range. Fail loud, fail early.

**Pure functions over classes** — There's no state to manage. A number goes in, a string comes out. Functions are simpler to test and sufficient here.

**Testing at multiple levels** — Unit tests for converter and extractor separately (isolate failures), plus integration tests for the full pipeline (catch wiring bugs).

## Assumptions

- Input is a plain-text file, one test case per line
- A valid number is a standalone digit sequence, not attached to special characters
- Lines with zero or multiple digit sequences are invalid
- Supports numbers up to trillions (999,999,999,999,999)
- Empty lines are skipped
