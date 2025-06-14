from cryptography.fernet import Fernet
import os

APPDATA_DIR = os.path.join(os.getenv("APPDATA"), "AccountManager")
MERGED_JSON = os.path.join(APPDATA_DIR, "merged.json")

with open("secret.key", "rb") as keyFile:
    key = keyFile.read()
    
cipher_suite = Fernet(key)

with open(MERGED_JSON, "rb") as file:
    original_data = file.read()

encrypted_data = cipher_suite.encrypt(original_data)

with open("glist_encrypted.json", "wb") as file:
    file.write(encrypted_data)

with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("glist.json encrypted and saved as glist_encrypted.json.")