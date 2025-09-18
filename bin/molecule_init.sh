#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install ansible molecule molecule-plugins

ansible --version
molecule --version

molecule list