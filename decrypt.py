# Directory traversal
import os

#Arguments
import sys

# Cryptography
from cryptography.fernet import Fernet, InvalidToken

#UI
import alive_progress

# Input
from getpass import getpass

# Time measure
import time

#Core
import core


files = []

def get_key():
    usr_input = getpass("Enter decrypt password > ")
    key = core.create_key(usr_input)
    return key


def decrypt_file(path: str, fernet):
    start = time.process_time()
    data = None
    with open(path, "rb") as f:
        data = f.read()
    decrypted_data = fernet.decrypt(data)
    
    with open(path, "wb") as f:
        f.write(decrypted_data)
    
    print(f"Decrypted '{path}' in {time.process_time() - start}s")
    
    
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
    print(f"Finding files in '{os.path.abspath(path)}' which is {"file" if os.path.isfile(path) else "dir" if os.path.isdir(path) else "Unknown"}")

    if not os.path.isdir(path) and not os.path.isfile(path):
        print("\"Where's my file\" doesn't support links/portals etc.")
        exit(1)
        
        
        
    if os.path.isfile(path):
        if not core.are_you_sure(f"You will decrypt single {os.path.abspath(path)} file."):
            print("Action cancelled")
            exit(0)
        # Get encrypting password
        encryptionKey = get_key()
        fernet = Fernet(encryptionKey)
        
        decrypt_file(path, fernet)
        print("Sucessfully decrypted single file")
        exit(0)
    #decrypt multiple files
    filesToDecrypt = core.get_encrypt_files(path)
    if len(filesToDecrypt) == 0:
        print("There's no files to decrypt.")
        exit(0)
    if not core.are_you_sure(f"Decrypting files will affect {len(filesToDecrypt)} files."):
        print("Action cancelled")
        exit(0)
    # Perform decrypting
    encryptionKey = get_key()
    fernet = Fernet(encryptionKey)
    
    decrypt_files(filesToDecrypt, fernet)
    
        
if __name__ == "__main__":
    ascii = r"""
  _      ____              _                     __          __ ___ 
 | | /| / / /  ___ _______( )___   __ _  __ __  / /______ __/ //__ \
 | |/ |/ / _ \/ -_) __/ -_)/(_-<  /  ' \/ // / / __/ -_) \ / __//__/
 |__/|__/_//_/\__/_/  \__/ /___/ /_/_/_/\_, /  \__/\__/_\_\\__/(_)  
                                       /___/                        
    """
    print(ascii)
    main()
