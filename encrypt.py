# Directory traversal
import os

# Cryptograpy
from cryptography.fernet import Fernet

# Arguments
import sys

# UI
import alive_progress
from termcolor import cprint

# Input
from getpass import getpass

# Time measure
import time

# Core
import core


def get_key():
    usr_input = getpass("Enter encrypt password > ")
    key = core.create_key(usr_input)
    return key


def encrypt_file(path: str, fernet):
    start = time.process_time()
    data = None

    try:

        with open(path, "rb") as f:
            data = f.read()
        encryped_data = fernet.encrypt(data)

        with open(path, "wb") as f:
            f.write(encryped_data)
    except:
        cprint(f"Failed encrypting '{path}'", "red", file=sys.stderr)
    cprint(
        f"Encrypted '{path}' in {time.process_time() - start}s",
        "green",
        file=sys.stdout,
    )


def encrypt_files(files, fernet):
    with alive_progress.alive_bar(
        len(files), bar="blocks", title="Encrypting.."
    ) as bar:
        for file in files:
            encrypt_file(file, fernet)
            bar()


def main() -> None:
    path: str = "."
    if len(sys.argv) > 1:
        path = sys.argv[1]

    cprint(
        f"Finding files in '{os.path.abspath(path)}' which is {core.get_file_type(path)}",
        "yellow",
        file=sys.stdout,
    )

    # Ignore sussy baka skibidi ohio rizz files
    if (
        (not os.path.isdir(path) and not os.path.isfile(path))
        or os.path.islink(path)
        or os.path.ismount(path)
        or path.endswith(".lnk")
    ):
        cprint(
            "\"Where's my file\" doesn't support links/portals etc.!",
            "red",
            attrs=["bold"],  # fat error
            file=sys.stderr,
        )
        exit(1)

    if os.path.isfile(path):
        if not core.are_you_sure(
            f"You will encrypt single {os.path.abspath(path)} file."
        ):
            cprint("Encrypting cancelled", "red")
            exit(0)
        # Get encrypting password
        encryptionKey = get_key()  # Reads secret password from stdin
        fernet = Fernet(encryptionKey)

        encrypt_file(path, fernet)
        cprint("Sucessfully encrypted single file", "green")
        exit(0)

    # Encrypt multiple files
    filesToEncrypt = core.get_encrypt_files(path)
    if len(filesToEncrypt) == 0:
        print("There's no files to encrypt.")
        exit(0)
    if not core.are_you_sure(
        f"Encryping files will affect {len(filesToEncrypt)} files."
    ):
        cprint("Encrypting cancelled", "red")
        exit(0)
    # Perform encrypting
    encryptionKey = get_key()  # Reads secret password from stdin
    fernet = Fernet(encryptionKey)

    encrypt_files(filesToEncrypt, fernet)


if __name__ == "__main__":
    core.greet()
    main()
