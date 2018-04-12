from unittest import TestCase

from app.utils import validators


class TestValidators(TestCase):
    def test_is_valid_email(self):
        expected = {
            "abc@gmail.com": True,
            "1234@gmail.com": True,
            "가@gmail.com": False,
            "1234@abc": False,
            "@abc.com": False,
            "@.": False,
        }

        actual = expected.copy()
        for email in expected.keys():
            actual[email] = validators.is_valid_email(email)

        self.assertEqual(expected, actual)

    def test_is_valid_phone(self):
        expected = {
            "01012345678": True,
            "0101234567": True,
            "010123456": False,
            "0212345678": True,
            "021234567": True,
            "02123456": False,
            "03112345678": True,
            "0311234567": True,
            "031123456": False,
            "050512341234": True,

            "010-1234-5678": True,
            "010-12345678": True,
            "0101234-5678": True,
            "010-123-4567": True,
            "010-123-456": False,
            "02-1234-5678": True,
            "02-123-4567": True,
            "02-123-456": False,

            "031-1234-5678": True,
            "031-123-4567": True,
            "031-123-456": False,
            "0505-1234-1234": True,

            "010.1234.5678": False,
            "010 1234 5678": False,
        }

        actual = expected.copy()
        for phone in expected.keys():
            actual[phone] = validators.is_valid_phone(phone)

        self.assertEqual(expected, actual)

    def test_has_valid_length(self):
        length_range = [4, 20]
        expected = {
            "1234": True,
            "123": False,
            "12345678901234567890": True,
            "123456789012345678901": False,

            "        ": True,
            "123 ": True,
            "12345678901234567890 ": False,
            "1234567890123456789 0": False,
        }

        actual = expected.copy()
        for string in expected.keys():
            actual[string] = validators.has_valid_length(string, *length_range)

        self.assertEqual(expected, actual)
