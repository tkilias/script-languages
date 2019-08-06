#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
ENCRYPTED_SECRET=$1
SECRET_NAME=$2
KEYRING_NAME=$3
KEY_NAME=$4
mkdir -p secrets
echo -n "$ENCRYPTED_SECRET" |
	base64 -d -w |
       	gcloud kms decrypt --plaintext-file=- --ciphertext-file=- --location=global --keyring=$KEYRING_NAME --key=$KEY_NAME > "secrets/$SECRET_NAME"
