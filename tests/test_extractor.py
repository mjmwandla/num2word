import unittest
from num2word.extractor import extract_number


class TestExtractNumber(unittest.TestCase):

    # valid cases from spec
    def test_number_in_middle_of_sentence(self):
        self.assertEqual(extract_number("The pump is 536 deep underground."), 536)

    def test_number_with_period_after(self):
        self.assertEqual(extract_number("We processed 9121 records."), 9121)

    def test_large_number(self):
        self.assertEqual(
            extract_number("The database has 66723107008 records."),
            66723107008,
        )

    def test_number_followed_by_text(self):
        self.assertEqual(
            extract_number("Interactive and printable 10022 ZIP code."),
            10022,
        )

    # invalid cases from spec
    def test_hash_prefixed_number(self):
        self.assertIsNone(
            extract_number("Variables reported as having a missing type #65678.")
        )

    def test_multiple_digit_groups(self):
        self.assertIsNone(extract_number("I received 23 456,9 KGs."))

    # edge cases
    def test_no_digits(self):
        self.assertIsNone(extract_number("No numbers here at all."))

    def test_number_at_start_of_line(self):
        self.assertEqual(extract_number("42 is the answer."), 42)

    def test_number_at_end_of_line(self):
        self.assertEqual(extract_number("The answer is 42"), 42)

    def test_only_a_number(self):
        self.assertEqual(extract_number("42"), 42)

    def test_number_with_comma_attached(self):
        self.assertEqual(extract_number("I saw 42, and left."), 42)


if __name__ == "__main__":
    unittest.main()
