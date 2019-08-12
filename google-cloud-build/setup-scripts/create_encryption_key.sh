#!/bin/bash
set -o nounset
KEY_RING_NAME="$1"
KEY_NAME="$2"
gcloud kms keyrings create $KEY_RING_NAME --location global
gcloud kms keys create $KEY_NAME --location global --keyring $KEY_RING_NAME --purpose encryption

PROJECT=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects list --filter="$PROJECT" --format="value(PROJECT_NUMBER)")

#Grant key to Cloud Build
gcloud kms keys add-iam-policy-binding "$KEY_NAME" --location=global --keyring="$KEY_RING_NAME" --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com --role=roles/cloudkms.cryptoKeyDecrypter

#Grant key to Cloud Functions
gcloud beta iam service-accounts create build-cloud-functions --display-name "build-cloud-functions"
gcloud kms keys add-iam-policy-binding "$KEY_NAME" --location=global --keyring="$KEY_RING_NAME" --member=serviceAccount:build-cloud-functions@tpu-integration.iam.gserviceaccount.com  --role=roles/cloudkms.cryptoKeyDecrypter
