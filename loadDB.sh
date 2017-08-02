#!/bin/bash
CRED='../credentials/'

rm "$CRED"distrib.db
sqlite3 "$CRED"distrib.db < create_table.sql
python fillDB.py
chmod a+rw "$CRED"distrib.db
