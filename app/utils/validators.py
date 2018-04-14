import re


def is_valid_email(field):
    email_pattern = "[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*"\
        + "@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}"

    if re.fullmatch(email_pattern, field):
        return True

    return False


def has_valid_length(field, length_min, length_max):
    if not field:
        return False

    if not (length_min <= len(field) <= length_max):
        return False

    return True


def is_valid_phone(field):
    landlinephone_prefix = "(02|031|032|033|041|042|043|044|" \
                           + "051|052|053|054|055|061|062|063|064|067)"

    patterns = [
        "01[016789]{1}\d{3,4}\d{4}",
        landlinephone_prefix + "\d{3,4}\d{4}",
        "(0505|0504)\d{3,4}\d{4}",
        "070\d{3,4}\d{4}",

        "01[016789]{1}-?\d{3,4}-?\d{4}",
        landlinephone_prefix + "-?\d{3,4}-?\d{4}",
        "(0505|0504)-?\d{3,4}-?\d{4}",
        "070-?\d{3,4}-?\d{4}",
    ]

    for pattern in patterns:
        if re.fullmatch(pattern, field):
            return True

    return False
