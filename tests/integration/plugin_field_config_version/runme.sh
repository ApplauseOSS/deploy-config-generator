#!/bin/bash

TEST_DIR=$(dirname $0)
cd ${TEST_DIR}

export PYTHONPATH=../../..

for version in NONE 0 1 99; do
	echo "Running with config version: ${version}"

	rm -rf tmp.${version}
	mkdir tmp.${version}

	(
	set -x

	python -m deploy_config_generator -c site_config.${version}.yml -o tmp.${version} . $@ &> tmp.${version}/cmd_output.txt
	echo $? > tmp.${version}/exit_code.txt

	diff -BurN expected_output.${version} tmp.${version}
	)
done
