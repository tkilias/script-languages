#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
TAG_NAME="$1"
EXPORTED_CONTAINERS=.build_output/exports/*.tar.gz
COMMIT="$2"
GITHUB_USER="$3"
GITHUB_TOKEN="$(cat secrets/GITHUB_TOKEN)"
github-release "$TAG_NAME" $EXPORTED_CONTAINERS --commit $COMMIT \
                                     --tag "$TAG_NAME" \
                                     --prerelease \
                                     --github-repository "$GITHUB_USER/script-languages" \
                                     --github-access-token "$GITHUB_TOKEN"
