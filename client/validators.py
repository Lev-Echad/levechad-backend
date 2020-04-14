import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

ID_NUMBER_REGEX = r'^\d{8,9}$'


# Checks if the phone number starts with +972/0, and then if the second part is one of:
# 1. a land line geographic based number - 2/3/4/8/9 and afterwards 7 digits.
# 2. a new number country prefix - 7 and afterwards 8 digits.
# 3. a mobile number - 5 and afterwards 8 digits.
PHONE_NUMBER_REGEX = re.compile(r"^(\+972[- ]?|0)([23489]|[57]\d)[- ]?((\d{3}-?\d{4})|(\d{4}-?\d{3}))$")
phone_number_validator = RegexValidator(PHONE_NUMBER_REGEX)


def id_number_validator(value):
    """
    Validates ID numbers by the ID_NUMBER_REGEX and the Sifrat Bikoret.
    :type value: str
    """
    def digits_of(n):
        return [int(d) for d in str(n)]

    if not re.match(ID_NUMBER_REGEX, value):
        raise ValidationError('Invalid ID number.', params={'value': value})
    if len(value) == 8:
        value = '0' + value

    # Calculate Sifrat Bikoret
    checksum = 0
    digits = digits_of(value)
    odd_digits = digits[:-1:2]
    even_digits = digits[1:-1:2]
    checksum += sum(odd_digits)
    for digit in even_digits:
        checksum += sum(digits_of(digit * 2))
    checksum = 10 - (checksum % 10)  # Get difference from upper round number
    if checksum == 10:
        checksum = 0

    if str(checksum) != value[-1]:
        raise ValidationError('Invalid ID number: Incorrect check digit')
