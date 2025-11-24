import boto3
import tarfile
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# Config
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
REGION = os.getenv("AWS_REGION", "eu-north-1") # Defaults to Stockholm
DECRYPTED_FILE = "restored_backup.tar.gz"

def get_latest_backup_filename(s3_client):
    """
    Asks AWS for all files in the bucket, sorts them by date, 
    and returns the most recent one.
    """
    print(f"🔎 Scanning bucket '{BUCKET_NAME}' in {REGION}...")
    
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' not in response:
        print("❌ Error: The bucket is empty! Run backup.py first.")
        return None

    # Sort files by 'LastModified' date (Newest first)
    files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
    
    latest_file = files[0]['Key']
    print(f"✅ Found latest backup: {latest_file}")
    return latest_file

def restore():
    # 1. Setup AWS Connection
    s3 = boto3.client('s3', region_name=REGION)

    # 2. Get the latest file automatically
    file_to_restore = get_latest_backup_filename(s3)
    if not file_to_restore:
        return

    # 3. Download
    print(f"☁️  Downloading {file_to_restore}...")
    s3.download_file(BUCKET_NAME, file_to_restore, file_to_restore)

    # 4. Decrypt
    print("🔓 Decrypting...")
    try:
        with open("backup_key.key", "rb") as k:
            key = k.read()
        cipher = Fernet(key)

        with open(file_to_restore, "rb") as f:
            encrypted_data = f.read()
        
        decrypted_data = cipher.decrypt(encrypted_data)
        
        with open(DECRYPTED_FILE, "wb") as f:
            f.write(decrypted_data)
    except FileNotFoundError:
        print("❌ Error: 'backup_key.key' not found. You cannot decrypt without the key!")
        return

    # 5. Unzip
    print("📦 Unzipping...")
    with tarfile.open(DECRYPTED_FILE, "r:gz") as tar:
        tar.extractall(path="./restored_data")
        
    print(f"✅ SUCCESS! Data restored to ./restored_data folder.")

    # Optional Cleanup: Remove the downloaded encrypted file to keep folder clean
    # os.remove(file_to_restore)

if __name__ == "__main__":
    restore()
