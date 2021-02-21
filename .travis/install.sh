#!/bin/bash

set -ex

if [[ "$(uname -s)" == 'Darwin' ]]; then
    sw_vers

    git clone --depth 1 https://github.com/pyenv/pyenv ~/.pyenv
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    case "${TOXENV}" in
        py27)
            curl -O https://bootstrap.pypa.io/get-pip.py
            python get-pip.py --user
            ;;
        py36)
            pyenv install 3.6.1
            pyenv global 3.6.1
            ;;
    esac
    pyenv rehash
fi

pip install virtualenv
python -m virtualenv ~/.venv
source ~/.venv/bin/activate
pip install -r requirements-dev.txt -U --upgrade-strategy only-if-needed
