import os
import errno 
import csv
import sqlite3
import time
import datetime

path = '../credentials/'
con = sqlite3.connect(path + 'distrib.db')
cursor = con.cursor()
data = cursor.execute("select * from logs")

date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
csv_path = path + 'logs-' + date + '.csv'
with open(csv_path, "wb") as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write headers.
    csv_writer.writerow(['user_id', 'browser_id', 'website_id', 'date', 'status'])
    csv_writer.writerows(data)
#    csv_writer.writerow([cursor])
    # Write data.
    #csv_writer.writerows(cursor)
print('logs-' + date + '.csv' + ' exported')
csv_file.close()
con.close()
