import re
from django.core.exceptions import ValidationError

ID_NUMBER_REGEX = r'^\d{8,9}$'


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

    if str(checksum) != value[-1]:
        raise ValidationError('Invalid ID number: Incorrect check digit')
