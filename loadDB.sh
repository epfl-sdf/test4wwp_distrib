#!/bin/bash
CRED='../credentials/'
source venvDistrib/bin/activate
if [ -f "$CRED"distrib.db ]; 
then
	python export_logs.py			 
fi
rm "$CRED"distrib.db
sqlite3 "$CRED"distrib.db < create_table.sql
python fillDB.py
chmod a+rw "$CRED"distrib.db
