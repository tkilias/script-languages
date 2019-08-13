#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
REBUILD=$2
FLAVOR=$1
ADDITIONAL_ARGUMENTS=""
if [ "$REBUILD" == "true" ]
then
  ADDITIONAL_ARGUMENTS="--force-rebuild"
fi
touch /workspace/build-status.txt
./exaslct build --flavor-path "flavors/$FLAVOR" --workers 7 $ADDITIONAL_ARGUMENTS || echo "fail" > /workspace/build-status.txt
