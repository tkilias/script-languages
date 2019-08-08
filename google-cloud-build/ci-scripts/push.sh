#!/bin/bash
set +x	
set -o errexit
set -o nounset
set -o pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
source "$SCRIPT_DIR/generate_source_target_docker_options.sh"

FLAVOR="$1"
echo "FLAVOR: $FLAVOR"
shift 1
generate_source_target_docker_options $SCRIPT_DIR $*

touch /workspace/build-status.txt
COMMAND="./exaslct push $SOURCE_OPTIONS $TARGET_OPTIONS --push-all --force-push --flavor-path 'flavors/$FLAVOR' --workers 7"
echo "Executing Command: $COMMAND"
bash -c "$COMMAND" || echo "fail" > /workspace/build-status.txt
