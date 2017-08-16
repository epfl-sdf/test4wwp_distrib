#!/bin/bash
LAST_BACKUP_TIME=""
CURR_TIME=$(date +%H)
COMMAND='python code.py 8081'

function finish () {
	pkill -f "$COMMAND" 
	echo 'Arrêt de ' $COMMAND
	exit
}

trap finish EXIT 
	source venvDistrib/bin/activate 
	$COMMAND &
	
	# Exporte le logs chaque heure
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
done
