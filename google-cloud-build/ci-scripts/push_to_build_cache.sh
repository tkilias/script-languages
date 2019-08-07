#!/bin/bash
set +x	
set -o errexit
set -o nounset
FLAVOR=$1
DOCKER_REPOSITORY=$2
DOCKER_USERNAME=$3
COMMIT=$4
export TARGET_DOCKER_PASSWORD=$(cat secrets/DOCKER_PASSWORD)
TARGET_TAG_PREFIX="$COMMIT"
TARGET_OPTIONS="--target-docker-repository-name '$DOCKER_REPOSITORY' --target-docker-username '$DOCKER_USERNAME' --target-docker-tag-prefix '$TARGET_TAG_PREFIX'"
touch /workspace/build-status.txtdd
docker images
./exaslct push $TARGET_OPTIONS --push-all --force-push --flavor-path "flavors/$FLAVOR" --workers 7 || echo "fail" > /workspace/build-status.txt
