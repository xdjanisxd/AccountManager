from cryptography.fernet import Fernet

with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

with open("glist_encrypted.json", "rb") as file:
    encrypted_data = file.read()

decrypted_data = cipher_suite.decrypt(encrypted_data)

with open("glist_decrypted.json", "wb") as file:
    file.write(decrypted_data)

print("glist_encrypted.json decrypted and saved as glist_decrypted.json.")