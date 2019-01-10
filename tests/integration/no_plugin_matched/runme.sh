#!/bin/bash

TEST_DIR=$(dirname $0)
cd ${TEST_DIR}

export PYTHONPATH=../../..

rm -rf tmp
mkdir tmp

(
set -x

python -m deploy_config_generator -o tmp . $@ 2>&1 > tmp/cmd_output.txt
)

if [[ $? = 0 ]]; then
	echo "Command did not fail as expected!"
	exit 1
fi

diff -wru expected_output tmp
