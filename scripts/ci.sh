#!/bin/bash -x

# Install age
sudo apt install -y age

# Install sops
sudo curl -Lo /usr/local/bin/sops https://github.com/getsops/sops/releases/download/v3.11.0/sops-v3.11.0.linux.$(uname -m | sed -e 's:x86_64:amd64:' -e 's:aarch64:arm64:')
sudo chmod a+x /usr/local/bin/sops

# Install/run tox
pip install tox
tox
