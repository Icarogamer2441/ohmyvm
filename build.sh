#!/bin/bash

python3 -m py_compile ./omasm.py
python3 -m py_compile ./om.py
mv __pycache__/om.cpython-312.pyc ./bin/om
mv __pycache__/omasm.cpython-312.pyc ./bin/omasm
chmod +x ./bin/om
chmod +x ./bin/omasm
