#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
KEY_RING_NAME=$1
KEY_NAME=$2
gcloud kms keyrings create $KEY_RING_NAME --location global
gcloud kms keys create $KEY_NAME --location global --keyring $KEY_RING_NAME --purpose encryption
