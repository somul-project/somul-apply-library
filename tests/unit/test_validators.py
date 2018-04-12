from unittest import TestCase

from app.utils import validators


class TestValidators(TestCase):
    def test_is_valid_email(self):
        emails = {
            "abc@gmail.com": True,
            "가@gmail.com": False,
            "1234@gmail.com": False,
            "1234@abc": False,
            "@abc.com": False,
            "@.": False,
        }

        for email, expected in emails.items():
            self.assertEqual(expected,
                             validators.is_valid_email(email),
                             "Email = [{}] expected [{}]"
                             .format(email, expected))

    def test_is_valid_phone(self):
        phones = {
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

        for phone, expected in phones.items():
            self.assertEqual(expected,
                             validators.is_valid_phone(phone),
                             "Phone = [{}] expected [{}]"
                             .format(phone, expected))

    def test_has_valid_length(self):
        length_range = [4, 20]
        strings = {
            "1234": True,
            "123": False,
            "12345678901234567890": True,
            "123456789012345678901": False,

            "        ": True,
            "123 ": True,
            "12345678901234567890 ": False,
            "1234567890123456789 0": False,
        }

        for string, expected in strings.items():
            self.assertEqual(
                expected,
                validators.has_valid_length(string, *length_range),
                "String = [{}], boundary = [{}], expected [{}]"
                .format(string, length_range, expected))
