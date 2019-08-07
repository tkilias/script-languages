#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

function generate_build_json(){
	cat "$env_file" "$encrypted_docker_password_file" $* > data.yaml
	jinja2 $triggers/build.json.jinja2 data.yaml > build.json
	rm data.yaml
}

function create(){
	echo "creating" $I
	generate_build_json "$I"
	create_output=$($setup_scripts/create_build_trigger.sh build.json)
	rm build.json
	echo "$create_output"
	trigger_id=$(echo "$create_output" | jq .id)
	echo "trigger_id: $trigger_id"  > "$env_flavor_config_path"
}

function update(){
	echo "updating" $I
	generate_build_json "$env_flavor_config_path" "$I"
	$setup_scripts/update_build_trigger.sh build.json
	rm build.json
}

function main(){
	setup_scripts=setup-scripts
	triggers=triggers
	$setup_scripts/create_encrypted_docker_password.sh
	env_file=".env/env.yaml"
	encrypted_docker_password_file=".env/encrypted_docker_password.yaml"
	for I in $(ls $triggers/flavor-config/*.yaml)
	do
		filename=$(basename -- "$I")
		env_flavor_config_path=".env/flavor-config/$filename"
		if [ -f "$env_flavor_config_path" ]
		then
			update
		else
			create
		fi
	done
}

main
