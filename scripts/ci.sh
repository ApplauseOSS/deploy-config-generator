#!/bin/bash -x

# Add path for binaries from 'pip install --user'
PATH=$PATH:~/.local/bin

# Install/run tox
pip install --user tox
tox
