# Directory traversal
import os

# Arguments
import sys

# Cryptography
from cryptography.fernet import Fernet, InvalidToken

# UI
import alive_progress
from termcolor import cprint

# Input
from getpass import getpass

# Time measure
import time

import core


def get_key():
    usr_input = getpass("Enter decrypt password > ")
    key = core.create_key(usr_input)
    return key


def decrypt_file(path: str, fernet):
    start = time.process_time()
    data = None

    try:
        with open(path, "rb") as f:
            data = f.read()
            decrypted_data = fernet.decrypt(data)

            with open(path, "wb") as f:
                f.write(decrypted_data)
    except:
        cprint(f"Failed decrypting '{path}'", "red", file=sys.stderr)
    else:
        cprint(
            f"Decrypted '{path}' in {time.process_time() - start}s",
            "green",
            file=sys.stdout,
        )


def decrypt_files(files, fernet):
    with alive_progress.alive_bar(
        len(files), bar="blocks", title="Decrypting.."
    ) as bar:
        for file in files:
            decrypt_file(file, fernet)
            bar()


def main():
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
            f"You will decrypt single {os.path.abspath(path)} file."
        ):
            cprint("Action cancelled", "red")
            exit(0)
        # Get encrypting password
        encryptionKey = get_key()
        fernet = Fernet(encryptionKey)

        decrypt_file(path, fernet)
        print("Sucessfully decrypted single file")
        exit(0)
    # decrypt multiple files
    filesToDecrypt = core.get_encrypt_files(path)
    if len(filesToDecrypt) == 0:
        print("There's no files to decrypt.")
        exit(0)
    if not core.are_you_sure(
        f"Decrypting files will affect {len(filesToDecrypt)} files."
    ):
        print("Action cancelled")
        exit(0)
    # Perform decrypting
    encryptionKey = get_key()
    fernet = Fernet(encryptionKey)

    decrypt_files(filesToDecrypt, fernet)


if __name__ == "__main__":
    core.greet()
    main()
