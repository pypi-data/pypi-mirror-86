def ecuadorian_identifier_validator(identifier: str) -> bool:
    if (type(identifier) != str):
        raise Exception("Identifier must be a string")
    if (len(identifier) != 10):
        return False
    identifier_without_last_digit = identifier[:-1]
    verifier_number = identifier[-1]
    even_digits = []
    odd_digits = []
    for index, digit in enumerate(identifier_without_last_digit):
        parsed_digit = int(digit)
        if (index + 1) % 2 == 0:
            even_digits.append(parsed_digit)
        else:
            odd_digit_multiplied_by_two = parsed_digit * 2
            if odd_digit_multiplied_by_two > 9:
                odd_digit_multiplied_by_two = odd_digit_multiplied_by_two - 9
            odd_digits.append(odd_digit_multiplied_by_two)
    odd_digit_sum = sum(odd_digits)
    even_digits_sum = sum(even_digits)
    sum_of_all_digits = odd_digit_sum + even_digits_sum
    calculated_verifier_number = sum_of_all_digits % 10
    if calculated_verifier_number != 0:
        calculated_verifier_number = 10 - calculated_verifier_number
    return calculated_verifier_number == int(verifier_number)