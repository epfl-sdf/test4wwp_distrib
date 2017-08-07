#!/bin/bash

source venvDistrib/bin/activate 
export PYTHONPATH=$HOME/credentials/:$PYTHONPATH
python code.py 8081
