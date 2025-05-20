from argon2 import PasswordHasher

password_hasher = PasswordHasher(
    time_cost=3, memory_cost=2**16, parallelism=2, hash_len=32, salt_len=16
)


def read_secret(secret_name):
    try:
        with open(f"/run/secrets/{secret_name}", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


# END read_secret
