#!/bin/bash

TEST_DIR=$(dirname $0)
cd ${TEST_DIR}

export PYTHONPATH=../../..

export SOPS_AGE_KEY_FILE=../age-key.txt

set -e

rm -rf tmp
mkdir tmp

set -x

python3 -m deploy_config_generator -v -c site_config.yml -o tmp . $@

diff -BurN expected_output tmp
