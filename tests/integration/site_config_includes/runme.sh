#!/bin/bash

TEST_DIR=$(dirname $0)
cd ${TEST_DIR}

export PYTHONPATH=../../..

set -e

for env in env1 env2; do
	rm -rf tmp.${env}
	mkdir tmp.${env}

	(
	set -x

	python -m deploy_config_generator -c site_config.yml -e ${env} -o tmp.${env} . $@

	diff -BurN expected_output.${env} tmp.${env}
	)
done
