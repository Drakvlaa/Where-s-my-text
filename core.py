import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from termcolor import colored, cprint
import sys


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
            filesToEncrypt.extend(get_encrypt_files(path=sub))
    return filesToEncrypt


def are_you_sure(msg: str) -> bool:
    answer = input(colored(f"{msg} Are you sure? [Y\\n]\n", "light_yellow"))
    return answer == "Y"


def get_file_type(path):
    if os.path.isfile(path):
        return colored("file", "white")
    if os.path.isdir(path):
        return colored("directory", "blue", attrs=["bold"])
    return colored("unknown", "red")


def greet() -> None:
    greet = r"""
     _      ____              _                     __          __ ___ 
    | | /| / / /  ___ _______( )___   __ _  __ __  / /______ __/ //__ \
    | |/ |/ / _ \/ -_) __/ -_)/(_-<  /  ' \/ // / / __/ -_) \ / __//__/
    |__/|__/_//_/\__/_/  \__/ /___/ /_/_/_/\_, /  \__/\__/_\_\\__/(_)  
                                        /___/                        
    """
    cprint(greet, "green", "on_black", attrs=["bold"], file=sys.stdout)
