from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

with open("glist.json", "rb") as file:
    original_data = file.read()

encrypted_data = cipher_suite.encrypt(original_data)

with open("glist_encrypted.json", "wb") as file:
    file.write(encrypted_data)

with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("glist.json decrypted and saved as glist_encrypted.json.")