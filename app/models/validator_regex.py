def password_regex() -> str:
    # at least one lowercase
    # at least one uppercase
    # at least one digit
    # at least one special chars
    # at least 8 chars long
    return r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$&%?!*])[a-zA-Z\d@$&%?!*]{8,}$"


def email_regex() -> str:
    # contains @
    # local domain doesnt start/end with a dot and doesnt have consecutive dots
    # local domain has limited allowed special chars
    # top-level domain is 2-6 chars long (.ru, .com, .be, .domain, etc.)
    return r"^[a-z0-9_+-]+(?:\.[a-z0-9_+-]+)*@(?:[a-z0-9-]+\.)+[a-z]{2,6}$"
