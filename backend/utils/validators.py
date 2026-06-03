import re


def is_valid_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(
        pattern,
        email
    ) is not None


def is_strong_password(password):
    """Mật khẩu tối thiểu 6 ký tự, có ít nhất 1 chữ hoa, 1 chữ thường và 1 số."""
    if len(password) < 6:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True