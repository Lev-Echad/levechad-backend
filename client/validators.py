import re
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from client.models import Volunteer

ID_NUMBER_REGEX = r'^\d{8,9}$'

# Checks if the phone number starts with +972/0, and then if the second part is one of:
# 1. a land line geographic based number - 2/3/4/8/9 and afterwards 7 digits.
# 2. a new number country prefix - 7 and afterwards 8 digits.
# 3. a mobile number - 5 and afterwards 8 digits.
PHONE_NUMBER_REGEX = re.compile(r"^(\+972[- ]?|0)([23489]|[57]\d)[- ]?((\d{3}-?\d{4})|(\d{4}-?\d{3}))$")
phone_number_validator = RegexValidator(PHONE_NUMBER_REGEX)

ADULT_AGE = 18
MINIMUM_AGE = 16


def unique_id_number_validator(id_number):
    """
    Validates the given ID number does not exist under any volunteer (see #50)
    """
    if Volunteer.objects.filter(tz_number=id_number).count() > 0:
        raise ValidationError('המתנדב רשום כבר למערכת!')


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


def _calculate_age(date_of_birth):
    """
    Calculates age in years. Calculates the same way as human does, therefore solves leap years issues.
    :type date_of_birth: datetime.date
    """
    today = date.today()
    years_difference = today.year - date_of_birth.year
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age = years_difference - 1
    else:
        age = years_difference

    return age


def parental_consent_validator(new_volunteer):
    """
    If volunteer age is under ADULT_AGE, check that received parental_consent details.
    :raise: ValidationError if volunteer is underage and given data is missing
    parental_consent or any parental_consent details.
    """
    volunteer_age = _calculate_age(new_volunteer['date_of_birth'])

    if volunteer_age < ADULT_AGE:
        try:
            parental_consent = new_volunteer['parental_consent']
            parent_id = parental_consent['parent_id']
            parent_name = parental_consent['parent_name']

        except KeyError:
            raise ValidationError(f"Volunteers aged {MINIMUM_AGE}-{ADULT_AGE} must enter parental consent details.")


def minimum_age_validator(date_of_birth):
    """
    If new volunteer's age is under MINIMUM_AGE raise ValidationError.
    """
    volunteer_age = _calculate_age(date_of_birth)
    if volunteer_age < MINIMUM_AGE:
        raise ValidationError(f"Volunteers must be at least {MINIMUM_AGE} years old.")
