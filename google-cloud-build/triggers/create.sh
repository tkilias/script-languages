#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
for I in $(ls flavor-config/*.yaml)
do
	filename=$(basename -- "$I")
	env_flavor_config_path=".env/flavor-config/$filename"
	if [ ! -f "$env_flavor_config_path" ]
	then
		echo "creating" $I
		cat .env/env "$I" > data.yaml
		jinja2 build.json.jinja2 data.yaml > build.json
		rm data.yaml
		create_output=$(bash scripts/create_build_trigger.sh build.json)
		rm build.json
		echo "$create_output"
		trigger_id=$(echo "$create_output" | jq .id)
		echo "trigger_id: $trigger_id"  > "$env_flavor_config_path"
	fi
done
