import os
from cryptography.fernet import Fernet
from icecream import ic as cout


# Step 1: Generate and save the Fernet key
def generate_key(file_name="fernet.key"):
    key = Fernet.generate_key()
    with open(file_name, "wb") as key_file:
        key_file.write(key)
    print(f"Key saved to {file_name}")


# Step 2: Load the Fernet key
def load_key(file_name="fernet.key"):
    with open(file_name, "rb") as key_file:
        return key_file.read()


# Step 3: Encrypt the API key
def encrypt_api_key(api_key, key_file="fernet.key"):
    key = load_key(key_file)
    fernet = Fernet(key)
    encrypted_api_key = fernet.encrypt(api_key.encode())
    print(f"Encrypted API Key: {encrypted_api_key}")
    return encrypted_api_key


# Step 4: Decrypt the API key
def decrypt_api_key(key_file="fernet.key"):
    with open(".env", "rb") as file:
        encrypted_api_key = file.read()
    key = load_key(key_file)
    fernet = Fernet(key)
    decrypted_api_key = fernet.decrypt(encrypted_api_key).decode()
    print(f"Decrypted API Key: {decrypted_api_key}")
    return decrypted_api_key


def store_encrypted_key(encrypted_api_key):
    with open(".env", "wb") as file:
        file.write(encrypted_api_key)

def load_api_key():
    with open(".env", "r") as file:
        return file.read()

# Example usage:
if __name__ == "__main__":
    # Generate a key (Run this once and keep the key safe)
    # generate_key()
    # Your API Key
    # api_key = load_api_key()
    #
    # # Encrypt the API key
    # encrypted_key = store_encrypted_key(encrypt_api_key(api_key))
    #
    # # Decrypt the API key
    decrypted_key = decrypt_api_key()
    cout(decrypted_key)
    #
    # # Verify the decrypted key matches the original
    # assert api_key == decrypted_key
