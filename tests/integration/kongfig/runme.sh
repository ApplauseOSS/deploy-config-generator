#!/bin/bash

TEST_DIR=$(dirname $0)
cd ${TEST_DIR}

export PYTHONPATH=../../..

set -e

rm -rf tmp
mkdir tmp

set -x

python -m deploy_config_generator -c site_config.yml -v -o tmp . $@

diff -BurN expected_output tmp
