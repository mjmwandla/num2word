import unittest
from num2word.converter import convert, convert_below_hundred, convert_below_thousand


class TestBelowHundred(unittest.TestCase):

    def test_single_digits(self):
        self.assertEqual(convert_below_hundred(0), "")
        self.assertEqual(convert_below_hundred(3), "three")
        self.assertEqual(convert_below_hundred(7), "seven")

    def test_teens(self):
        self.assertEqual(convert_below_hundred(10), "ten")
        self.assertEqual(convert_below_hundred(12), "twelve")
        self.assertEqual(convert_below_hundred(16), "sixteen")

    def test_tens(self):
        self.assertEqual(convert_below_hundred(40), "forty")
        self.assertEqual(convert_below_hundred(70), "seventy")

    def test_compound(self):
        self.assertEqual(convert_below_hundred(23), "twenty-three")
        self.assertEqual(convert_below_hundred(57), "fifty-seven")
        self.assertEqual(convert_below_hundred(84), "eighty-four")


class TestBelowThousand(unittest.TestCase):

    def test_exact_hundreds(self):
        self.assertEqual(convert_below_thousand(200), "two hundred")
        self.assertEqual(convert_below_thousand(700), "seven hundred")

    def test_hundreds_with_remainder(self):
        self.assertEqual(convert_below_thousand(304), "three hundred and four")
        self.assertEqual(convert_below_thousand(418), "four hundred and eighteen")
        self.assertEqual(convert_below_thousand(536), "five hundred and thirty-six")
        self.assertEqual(convert_below_thousand(871), "eight hundred and seventy-one")

    def test_delegates_below_hundred(self):
        self.assertEqual(convert_below_thousand(63), "sixty-three")
        self.assertEqual(convert_below_thousand(8), "eight")


class TestConvert(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(convert(0), "zero")

    def test_small_numbers(self):
        self.assertEqual(convert(4), "four")
        self.assertEqual(convert(17), "seventeen")
        self.assertEqual(convert(85), "eighty-five")

    def test_hundreds(self):
        self.assertEqual(convert(300), "three hundred")
        self.assertEqual(convert(536), "five hundred and thirty-six")

    def test_thousands(self):
        self.assertEqual(convert(2750), "two thousand, seven hundred and fifty")
        self.assertEqual(convert(9121), "nine thousand, one hundred and twenty-one")

    def test_and_before_final_small_group(self):
        self.assertEqual(convert(10022), "ten thousand and twenty-two")
        self.assertEqual(convert(5003), "five thousand and three")
        self.assertEqual(convert(7014), "seven thousand and fourteen")

    def test_millions(self):
        self.assertEqual(convert(3500000), "three million, five hundred thousand")
        self.assertEqual(convert(8000047), "eight million and forty-seven")
        self.assertEqual(
            convert(4219836),
            "four million, two hundred and nineteen thousand, eight hundred and thirty-six",
        )

    def test_billions(self):
        self.assertEqual(convert(2000000000), "two billion")
        self.assertEqual(
            convert(66723107008),
            "sixty-six billion, seven hundred and twenty-three million, "
            "one hundred and seven thousand and eight",
        )

    def test_spec_examples(self):
        self.assertEqual(convert(536), "five hundred and thirty-six")
        self.assertEqual(convert(9121), "nine thousand, one hundred and twenty-one")
        self.assertEqual(convert(10022), "ten thousand and twenty-two")
        self.assertEqual(
            convert(66723107008),
            "sixty-six billion, seven hundred and twenty-three million, "
            "one hundred and seven thousand and eight",
        )

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            convert(-1)

    def test_rejects_non_integer(self):
        with self.assertRaises(TypeError):
            convert(3.14)
        with self.assertRaises(TypeError):
            convert("42")

    def test_rejects_too_large(self):
        with self.assertRaises(ValueError):
            convert(1_000_000_000_000_000)


if __name__ == "__main__":
    unittest.main()
