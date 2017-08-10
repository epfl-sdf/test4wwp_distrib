#!/bin/bash
virtFold=venvDistrib
sudo apt-get install python-pip
sudo apt-get install virtualenv
export LC_ALL=C
rm -rf $venvDistrib
virtualenv -p /usr/bin/python2 $virtFold
source $virtFold/bin/activate
pip2 install web.py
pip2 install httpagentparser
sudo apt install sqlite3
