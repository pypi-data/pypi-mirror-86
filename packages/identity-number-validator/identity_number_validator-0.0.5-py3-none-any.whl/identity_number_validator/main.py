from .countries import ecuadorian_identifier_validator


def identity_number_validator(identity_number: str, country: str):
    if (type(country) != str):
        raise Exception("Country code must be a string")
    upper_case_country = country.upper()
    if (upper_case_country == "EC"):
        return ecuadorian_identifier_validator(identity_number)
    raise Exception("Invalid country code")
