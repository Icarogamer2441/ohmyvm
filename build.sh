#!/bin/bash

python3 -m py_compile ./omasm.py
python3 -m py_compile ./om.py
python3 -m py_compile ./omang.py
mv __pycache__/om.cpython-*.pyc ./bin/om
mv __pycache__/omasm.cpython-*.pyc ./bin/omasm
mv __pycache__/omang.cpython-*.pyc ./bin/omang
chmod +x ./bin/om
chmod +x ./bin/omasm
chmod +x ./bin/omang
