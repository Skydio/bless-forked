#!/bin/bash

set -eu

yum install -y git tar gcc zlib-devel openssl-devel ncurses-devel libffi-devel bzip2-devel readline-devel
[[ ! -d ~/.pyenv ]] &&git clone https://github.com/pyenv/pyenv.git ~/.pyenv
export PATH=$PATH:$HOME/.pyenv/bin
eval "$(pyenv init -)"

pyenv install -s 3.12
pyenv global 3.12

python -m venv /tmp/venv
/tmp/venv/bin/pip install --upgrade pip setuptools
/tmp/venv/bin/pip install --upgrade --implementation cp --only-binary=:all: --target ./aws_lambda_libs -e .
#cp  -r /tmp/venv/lib/python3*/site-packages/. ./aws_lambda_libs
#cp -r /tmp/venv/lib64/python3*/site-packages/. ./aws_lambda_libs
