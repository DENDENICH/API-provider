import secrets

def generate_unique_code() -> int:
    return secrets.randbelow(9_000_000_000) + 1_000_000_000
