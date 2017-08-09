#!/bin/bash
LAST_BACKUP_TIME=-1
CURR_TIME=$(date +%H)

source venvDistrib/bin/activate 
python code.py 8081

# Exporte le logs chaques heures
while :
do
	CURR_TIME=$(date +%H)
	if ! [[ "$LAST_BACKUP_TIME" == "$CURR_TIME" ]];
	then
		LAST_BACKUP_TIME=$CURR_TIME
		python export_logs.py
	fi
	sleep 2
done
