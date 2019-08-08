#!/bin/bash
set +x	
set -o errexit
set -o nounset
set -o pipefail
FLAVOR="$1"
SOURCE_DOCKER_REPOSITORY="$2"
SOURCE_TAG_PREFIX="$3"
TARGET_DOCKER_REPOSITORY="$4"
TARGET_TAG_PREFIX="$5"
DOCKER_USERNAME="$6"
export TARGET_DOCKER_PASSWORD="$(cat secrets/DOCKER_PASSWORD)"
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
TARGET_OPTIONS="$($SCRIPT_DIR/docker_options.sh TARGET $TARGET_DOCKER_REPOSITORY $DOCKER_USERNAME $TARGET_TAG_PREFIX)"
SOURCE_OPTIONS="$($SCRIPT_DIR/docker_options.sh SOURCE $SOURCE_DOCKER_REPOSITORY $DOCKER_USERNAME $SOURCE_TAG_PREFIX)"
touch /workspace/build-status.txtdd
./exaslct push $SOURCE_OPTIONS $TARGET_OPTIONS --push-all --force-push --flavor-path "flavors/$FLAVOR" --workers 7 || echo "fail" > /workspace/build-status.txt
