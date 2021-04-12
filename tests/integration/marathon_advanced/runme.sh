#!/bin/bash

TEST_DIR=$(dirname $0)
cd ${TEST_DIR}

export PYTHONPATH=../../..

set -e

for env in NONE test_env; do
	echo "Running with env: ${env}"

	rm -rf tmp.${env}
	mkdir tmp.${env}

	if [[ $env != NONE ]]; then
		env_flag="-e ${env}"
	fi

	(
	set -x

	python -m deploy_config_generator -v -c site_config.yml -o tmp.${env} ${env_flag} . $@

	diff -BurN expected_output.${env} tmp.${env}
	)
done
