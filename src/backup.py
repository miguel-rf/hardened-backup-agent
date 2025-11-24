import os
import boto3
import tarfile
from datetime import datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

# Configuration
SOURCE_FOLDER = "./data_to_backup" # We will create this folder to test
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
BACKUP_FILENAME = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
ENCRYPTED_FILENAME = f"{BACKUP_FILENAME}.enc"

# Generate a temporary encryption key (In prod, store this safely!)
key = Fernet.generate_key()
cipher = Fernet(key)

def create_archive():
    print(f"📦 Compressing {SOURCE_FOLDER}...")
    with tarfile.open(BACKUP_FILENAME, "w:gz") as tar:
        tar.add(SOURCE_FOLDER, arcname=os.path.basename(SOURCE_FOLDER))

def encrypt_file():
    print(f"🔒 Encrypting backup...")
    with open(BACKUP_FILENAME, "rb") as f:
        original = f.read()
    encrypted = cipher.encrypt(original)
    with open(ENCRYPTED_FILENAME, "wb") as f:
        f.write(encrypted)
    # Save the key locally so you can decrypt it later if needed
    with open("backup_key.key", "wb") as k:
        k.write(key)

def upload_to_aws():
    print(f"☁️ Uploading to {BUCKET_NAME}...")
    s3 = boto3.client('s3') # Automagically finds creds in .env
    s3.upload_file(ENCRYPTED_FILENAME, BUCKET_NAME, ENCRYPTED_FILENAME)
    print("✅ Upload Complete!")

if __name__ == "__main__":
    if not os.path.exists(SOURCE_FOLDER):
        os.makedirs(SOURCE_FOLDER)
        with open(f"{SOURCE_FOLDER}/secret.txt", "w") as f:
            f.write("Confidential data for CV project.")

    try:
        create_archive()
        encrypt_file()
        upload_to_aws()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup: Remove the unencrypted zip
        if os.path.exists(BACKUP_FILENAME):
            os.remove(BACKUP_FILENAME)
