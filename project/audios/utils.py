from cryptography.fernet import Fernet
from pathlib import Path
import uuid
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Load the key
def load_key():
    return env("ENCRYPTION_KEY")

# Encrypt a file
def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)
    
    with open(file_path, "rb") as file:
        file_data = file.read()
        
    encrypted_data = fernet.encrypt(file_data)
    
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_data)
    
    os.remove(file_path)
    return encrypted_file_path

# Decrypt a file
def decrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)
    
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
        
    decrypted_data = fernet.decrypt(encrypted_data)
    
    decrypted_file_path = file_path.replace(".enc", "")
    with open(decrypted_file_path, "wb") as file:
        file.write(decrypted_data)
    
    return decrypted_file_path

# Generate a unique filename for encrypted files
def generate_unique_filename(filename):
    ext = filename.split('.')[-1]
    return f"{uuid.uuid4()}.{ext}"
