import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


def create_key(password: str):
    bytes = str.encode(password)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"",
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(bytes))


def filter_python(path: str) -> bool:
    if path.endswith(".py"):
        return False
    return True


def get_encrypt_files(path: str | None = None, filter=filter_python) -> list[str]:
    filesToEncrypt: list[str] = []
    for file in os.listdir(path):
        sub = os.path.join(path, file)
        # Filter files
        if not filter(path=sub):
            continue
        if os.path.isfile(sub):
            filesToEncrypt.append(sub)
        # Directory recursive traversal
        if os.path.isdir(sub):
            for file in get_encrypt_files(path=sub):
                filesToEncrypt.append(file)
    return filesToEncrypt


def are_you_sure(msg: str) -> bool:
    answer = input(f"{msg} Are you sure? [Y\\n]\n")
    return answer == "Y"
