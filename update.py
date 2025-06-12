
import os
import sys
import requests
from cryptography.fernet import Fernet

APPDATA_DIR = os.path.join(os.getenv("APPDATA"), "AccountManager")
os.makedirs(APPDATA_DIR, exist_ok=True)

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def decrypt_file(encrypted_file_path, key_path, decrypted_file_path):
    with open(key_path, "rb") as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    with open(encrypted_file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(decrypted_file_path, "wb") as file:
        file.write(decrypted_data)

def check_for_updates():
    encrypted_file_url = "https://raw.githubusercontent.com/xdjanisxd/AccountManager/main/glist_encrypted.json"
    enc_file_path = os.path.join(APPDATA_DIR, "glist_encrypted.json")
    dec_file_path = os.path.join(APPDATA_DIR, "glist.json")
    key_path = os.path.join(BASE_DIR, "secret.key")

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(encrypted_file_url, headers=headers)
        if response.status_code == 200 and response.content:
            with open(enc_file_path, "wb") as file:
                file.write(response.content)
            try:
                decrypt_file(enc_file_path, key_path, dec_file_path)
            except Exception as e:
                with open(os.path.join(APPDATA_DIR, "decrypt_error.txt"), "w") as log:
                    log.write(f"Decryption failed: {e}")
        else:
            print("Download failed or empty content.")
    except Exception as e:
        with open(os.path.join(APPDATA_DIR, "update_error.txt"), "w") as log:
            log.write(f"Update failed: {e}")

if __name__ == "__main__":
    check_for_updates()
