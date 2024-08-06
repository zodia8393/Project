from cryptography.fernet import Fernet
import os

def generate_and_save_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_sensitive_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

# 키가 없으면 생성
if not os.path.exists("secret.key"):
    generate_and_save_key()

ENCRYPTION_KEY = load_key()