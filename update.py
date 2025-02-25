import requests
from cryptography.fernet import Fernet

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
    
    try:
        response = requests.get(encrypted_file_url)
        if response.status_code == 200:
            with open("glist_encrypted.json", "wb") as file:
                file.write(response.content)
            
            decrypt_file("glist_encrypted.json", "secret.key", "glist.json")
            print("glist.json updated.")
        else:
            print(f"An error occured while downloading encrypted file. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    check_for_updates()