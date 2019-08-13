#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

function generate_build_json(){
	cat "$ENV_FILE" "$ENCRYPTED_DOCKER_PASSWORD_FILE" "$ENCRYPTED_GITHUB_TOKEN_FILE" $* > data.yaml
  echo "job_id: \"${TRIGGER_CONFIG_PATH##*$TRIGGERS/flavor-config/}\""  >> data.yaml
	TRIGGER_FILE=$(cat "$TRIGGER_CONFIG_PATH" | yq -r .trigger_template_file)
	jinja2 $TRIGGERS/$TRIGGER_FILE data.yaml > build.json
	rm data.yaml
}

function create(){
	echo "creating" $TRIGGER_CONFIG_PATH
	generate_build_json "$TRIGGER_CONFIG_PATH"
	CREATE_OUTPUT=$($SETUP_SCRIPTS/create_build_trigger.sh build.json)
	rm build.json
	echo "$CREATE_OUTPUT"
	TRIGGER_ID=$(echo "$CREATE_OUTPUT" | jq .id)
	mkdir -p $(dirname "$ENV_FLAVOR_CONFIG_PATH")
	echo "trigger_id: $TRIGGER_ID"  > "$ENV_FLAVOR_CONFIG_PATH"
}

function update(){
	echo "updating" $TRIGGER_CONFIG_PATH
	generate_build_json "$ENV_FLAVOR_CONFIG_PATH" "$TRIGGER_CONFIG_PATH"
	$SETUP_SCRIPTS/update_build_trigger.sh build.json
	rm build.json
}

function create_or_update(){
  ENV_FLAVOR_CONFIG_PATH=".env/$TRIGGER_CONFIG_PATH"
  if [ -f "$ENV_FLAVOR_CONFIG_PATH" ]
  then
    update
  else
    create
  fi
}


function main(){
	SETUP_SCRIPTS=setup-scripts
	TRIGGERS=triggers
	$SETUP_SCRIPTS/create_encrypted_docker_password.sh
	$SETUP_SCRIPTS/create_encrypted_github_token.sh
	ENV_FILE=".env/env.yaml"
	ENCRYPTED_DOCKER_PASSWORD_FILE=".env/encrypted_docker_password.yaml"
	ENCRYPTED_GITHUB_TOKEN_FILE=".env/encrypted_github_token.yaml"
	for TRIGGER_CONFIG_PATH in $(find $TRIGGERS/flavor-config -name '*.yaml')
  do
	  create_or_update
	done
}

main
