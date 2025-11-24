Hardened Backup Agent

A secure automation tool designed to compress, encrypt, and ship critical server data to an offsite cloud vault.

This agent operates on a Client-Side Encryption model. Data is encrypted locally using the Fernet (Symmetric) algorithm before it ever touches the network, ensuring confidentiality even if the cloud storage provider is compromised.

Designed to upload to the Secure Cloud Vault.

Architecture

Compression: Targets a local directory and creates a tar.gz archive.

Encryption: Generates a symmetric key and encrypts the archive (Fernet/AES).

Transport: Uploads the encrypted payload to AWS S3 using boto3.

Restoration: Includes a recovery module to automatically fetch, decrypt, and extract the latest backup.

Usage Guide (Arch Linux)

1. Clone the Repository
git clone [https://github.com/yourusername/hardened-backup-agent.git](https://github.com/yourusername/hardened-backup-agent.git)
cd hardened-backup-agent


2. Setup Environment

Arch Linux requires virtual environments for Python projects.

# Install dependencies
sudo pacman -S python python-pip

# Create and activate environment
python -m venv venv
source venv/bin/activate

# Install libraries
pip install boto3 cryptography python-dotenv


3. Configuration

Create a .env file:

AWS_ACCESS_KEY_ID=your_terraform_output_key
AWS_SECRET_ACCESS_KEY=your_terraform_output_secret
AWS_BUCKET_NAME=your_terraform_output_bucket
AWS_REGION=eu-north-1


4. Running the Backup

python src/backup.py


5. Running a Restore

python src/restore.py