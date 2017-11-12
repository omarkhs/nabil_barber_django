#!/bin/bash

virtualenv environment
if [ $? -ne 0 ]; then
    # Set to red and run
    tput setaf 1; echo ${RED}FAILED
    exit
fi

source environment/bin/activate
if [ $? -ne 0 ]; then
    # Set to red and run
    tput setaf 1; echo ${RED}FAILED
    exit
fi

PIP_REQUIRE_VIRTUALENV=true pip install -r requirements.txt
if [ $? -eq 0 ]; then
    python --version
    which python
    pip --version
    which pip
else
    # Set to red and run
    tput setaf 1; echo ${RED}FAILED
fi
