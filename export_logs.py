# -*- coding: utf-8 -*-
import os
import errno 
import csv
import sqlite3
import time
import datetime


path = '../credentials/'
con = sqlite3.connect(path + 'distrib.db')
cursor = con.cursor()
date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
data = cursor.execute("SELECT s.id, s.name, s.jahia, s.wordpress, b.id, b.os, b.name, b.version, l.date, u.id, u.first_name, u.last_name, l.status FROM logs l INNER JOIN browsers b ON l.browser_id=b.id INNER JOIN users u ON l.user_id=u.id INNER JOIN websites s ON l.website_id=s.id ORDER BY l.date;")
adjusted_data = []
for elem in data:
	adjusted_data.append((elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], datetime.datetime.fromtimestamp(elem[8]).strftime('%Y-%m-%d_%H:%M:%S'), elem[9], elem[10].encode('utf-8'), elem[11].encode('utf-8'), elem[12]))

def write_logs(filename, data):
    csv_path = path + filename
    with open(csv_path, "wb") as csv_file:
       csv_writer = csv.writer(csv_file)
       # Write headers.
       csv_writer.writerow(['website_id', 'site_title', 'jahia', 'wordpress', 'browser_id', 'os', 'browser_name', 'version', 'date', 'user_id', 'first_name', 'last_name', 'status'])
       csv_writer.writerows(data)
       print(filename + ' exported')
    csv_file.close()

write_logs('logs-' + date + '.csv', adjusted_data)
write_logs('distrib.log', adjusted_data)
con.close()
