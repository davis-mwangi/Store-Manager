import re


EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')
SPECIAL_CHARS = '[@_!#$%^&*()<>?/\|}{~:]'
NUMERIC_REGEX = re.compile(r"^[0-9]+$")


def check_blank(value):
    if value.strip() == "":
        raise ValueError("{} Cannot be blank".format(value))
    return value


def email(value):
    if value.strip() == "":
        raise ValueError("Email cannot be blank")

    if not EMAIL_REGEX.match(value):
        raise ValueError("Invalid email format")

    return value


def validate_name(value):
    if value.strip() == "":
        raise ValueError("Name cannot be blank")

    if not value.isalpha():
        raise ValueError("Invalid name")

    return value


def numeric_only(value):
    check_blank(value)
    if not NUMERIC_REGEX.match(value):
        raise ValueError("Only numbers required for this field")
    return value


def validate_password(password):

    if not any(char.isdigit() for char in password):
        raise ValueError('password should have at least one numeral')

    if not any(char.isupper() for char in password):
        raise ValueError(
            'password should have at least one uppercase letter')

    if not any(char.islower() for char in password):
        raise ValueError(
            'the password should have at least one lowercase letter')

    if not any(char in SPECIAL_CHARS for char in password):
        raise ValueError(
            'password should have at least one special character e.g $%$#')
    if len(password) < 8:
        raise ValueError(
            'length of password should be 8 charatcers or more')
    return password


def validate_product_name(value):
    check_blank(value)
    if value.isdigit():
        raise ValueError("Product name  cannot be numerics only")
    return value
