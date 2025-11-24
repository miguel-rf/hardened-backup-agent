# Hardened Backup Agent

A secure automation tool designed to compress, encrypt, and ship critical server data to an offsite cloud vault.

This agent operates on a **Client-Side Encryption** model. Data is encrypted locally using the Fernet (Symmetric) algorithm before it ever touches the network, ensuring confidentiality even if the cloud storage provider is compromised.

**Integration:** Designed to upload to the [Secure Cloud Vault](https://github.com/yourusername/secure-cloud-vault).

## Architecture

*   **Compression:** Targets a local directory and creates a `tar.gz` archive.
*   **Encryption:** Generates a symmetric key and encrypts the archive (Fernet/AES).
*   **Transport:** Uploads the encrypted payload to AWS S3 using `boto3`.
*   **Restoration:** Includes a recovery module to automatically fetch, decrypt, and extract the latest backup.

## Usage Guide

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hardened-backup-agent.git
cd hardened-backup-agent
```

### 2. Setup Environment

Arch Linux requires virtual environments for Python projects.

```bash
# Install dependencies
sudo pacman -S python python-pip

# Create and activate environment
python -m venv venv
source venv/bin/activate

# Install libraries
pip install boto3 cryptography python-dotenv
```

### 3. Configuration

Create a `.env` file in the root directory:

```ini
AWS_ACCESS_KEY_ID=your_terraform_output_key
AWS_SECRET_ACCESS_KEY=your_terraform_output_secret
AWS_BUCKET_NAME=your_terraform_output_bucket
AWS_REGION=eu-north-1
```

### 4. Running the Backup

To encrypt and upload your data:

```bash
python src/backup.py
```

### 5. Running a Restore

To fetch, decrypt, and extract the latest version:

```bash
python src/restore.py
```
