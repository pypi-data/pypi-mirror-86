#!/usr/bin/env bash

set -e  # stop execution in case of errors

pip install -r requirements.txt
pip install coverage coveralls
pip install pytest
pip install pytest-sugar
pip install pytest-dependency
pip install pytest-cov
pip install flaky
python setup.py install
