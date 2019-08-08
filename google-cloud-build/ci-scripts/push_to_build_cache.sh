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
TARGET_OPTIONS="$($SCRIPT_DIR/docker_options.sh 'target' $TARGET_DOCKER_REPOSITORY $DOCKER_USERNAME $TARGET_TAG_PREFIX)"
SOURCE_OPTIONS="$($SCRIPT_DIR/docker_options.sh 'source' $SOURCE_DOCKER_REPOSITORY $DOCKER_USERNAME $SOURCE_TAG_PREFIX)"

echo "FLAVOR: $FLAVOR"
echo "SOURCE_DOCKER_REPOSITORY: $SOURCE_DOCKER_REPOSITORY"
echo "SOURCE_TAG_PREFIX: $SOURCE_TAG_PREFIX"
echo "TARGET_DOCKER_REPOSITORY: $TARGET_DOCKER_REPOSITORY"
echo "TARGET_TAG_PREFIX: $TARGET_TAG_PREFIX"
echo "DOCKER_USERNAME: $DOCKER_USERNAME"
echo "TARGET_OPTIONS: $TARGET_OPTIONS"
echo "SOURCE_OPTIONS: $SOURCE_OPTIONS"

touch /workspace/build-status.txt
COMMAND="./exaslct push $SOURCE_OPTIONS $TARGET_OPTIONS --push-all --force-push --flavor-path 'flavors/$FLAVOR' --workers 7"
echo "Executing Command: $COMMAND"
bash -c "$COMMAND" || echo "fail" > /workspace/build-status.txt
