"""End-to-end tests — full pipeline from text line to English words."""
import unittest
from num2word.main import process_line


class TestProcessLine(unittest.TestCase):
    """Test the full extraction → conversion pipeline."""

    def test_spec_cases(self):
        cases = {
            "The pump is 536 deep underground.": "five hundred and thirty-six",
            "We processed 9121 records.": "nine thousand, one hundred and twenty-one",
            "Variables reported as having a missing type #65678.": "number invalid",
            "Interactive and printable 10022 ZIP code.": "ten thousand and twenty-two",
            "The database has 66723107008 records.": (
                "sixty-six billion, seven hundred and twenty-three million, "
                "one hundred and seven thousand and eight"
            ),
            "I received 23 456,9 KGs.": "number invalid",
        }
        for line, expected in cases.items():
            with self.subTest(line=line):
                self.assertEqual(process_line(line), expected)

    def test_no_number(self):
        self.assertEqual(process_line("No numbers here."), "number invalid")

    def test_number_at_boundaries(self):
        self.assertEqual(process_line("7 apples"), "seven")
        self.assertEqual(process_line("bought apples 7"), "seven")

    def test_empty_line(self):
        self.assertEqual(process_line(""), "number invalid")


if __name__ == "__main__":
    unittest.main()
