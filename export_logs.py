import os
import errno 
import csv
import sqlite3
import time
import datetime

path = '../credentials/'
con = sqlite3.connect(path + 'distrib.db')
cursor = con.cursor()
data = cursor.execute("SELECT s.id, s.jahia, s.wordpress, b.os, b.name, b.version, l.date, u.id, u.first_name, u.last_name, l.status FROM logs l INNER JOIN browsers b ON l.browser_id=b.id INNER JOIN users u ON l.user_id=u.id INNER JOIN websites s ON l.website_id=s.id ORDER BY l.date DESC;")
adjusted_data = []
for elem in data:
	adjusted_data.append((elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], datetime.datetime.fromtimestamp(elem[6]).strftime('%Y-%m-%d_%H:%M:%S'), elem[7], elem[8], elem[9], elem[10]))
date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
csv_path = path + 'logs-' + date + '.csv'
with open(csv_path, "wb") as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write headers.
    csv_writer.writerow(['website_id', 'jahia', 'wordpress', 'os', 'browser_name', 'version', 'date', 'user_id', 'first_name', 'last_name', 'status'])
    csv_writer.writerows(adjusted_data)
#    csv_writer.writerow([cursor])
    # Write data.
    #csv_writer.writerows(cursor)
print('logs-' + date + '.csv' + ' exported')
csv_file.close()
con.close()
