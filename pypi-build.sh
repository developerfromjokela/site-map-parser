#!/bin/bash
python3 -m virtualenv --python3.8 venv
source venv/bin/activate
python3 --version
python3 -m pytest
