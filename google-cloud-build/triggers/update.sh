#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
scripts/create_encrypted_docker_password.sh
env_file=".env/env.yaml"
encrypted_docker_password_file=".env/encrypted_docker_password.yaml"
for I in $(ls flavor-config/*.yaml)
do
	filename=$(basename -- "$I")
	env_flavor_config_path=".env/flavor-config/$filename"
	if [ -f "$env_flavor_config_path" ]
	then
		echo "updating" $I
		cat "$env_file" "$encrypted_docker_password_file"  "$env_flavor_config_path" "$I" > data.yaml
		jinja2 build.json.jinja2 data.yaml > build.json
		rm data.yaml
		bash scripts/update_build_trigger.sh build.json
		rm build.json
	fi
done
