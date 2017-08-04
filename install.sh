#!/bin/bash
virtFold=venvDistrib
sudo apt-get install python-pip
sudo apt-get install virtualenv
export LC_ALL=C
rm -rf $venvDistrib
virtualenv -p /usr/bin/python2 $virtFold
source $virtFold/bin/activate
pip2 install web.py
deactivate
sudo apt install sqlite3
