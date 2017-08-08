import os
import errno
import csv
import sqlite3

path = '../credentials/'
con = sqlite3.connect(path + 'distrib.db')
cur = con.cursor()

# Insert urls
credentials = open(path + 'credentials.csv')
reader = csv.reader(credentials)
i = 0
next(reader)
for row in reader:
    # (id, name, Jahia, WP, userview, password, random)
    cur.execute(('INSERT INTO websites VALUES(' 
                + str(i) + ', "'+ row[1] + '", "' + row[2]+ '", "' + row[3] + '", "' + row[6] + '", "' + row[7] + '", ' + row[0] + ');\n'))
    i += 1
con.commit()
credentials.close()
print('Websites (Credentials) OK')

# Insert Users
users = open(path + 'users.csv')
reader = csv.reader(users)
next(reader)
for row in reader:
    cur.execute('INSERT INTO users VALUES (' + row[0] + ', "' + row[2] + '", "' + row[1] + '");')
con.commit()
users.close()
print('Users OK')

cur.execute('INSERT INTO browsers VALUES (0, "Firefox", "54.0", "Windows");')
cur.execute('INSERT INTO browsers VALUES (1, "Firefox", "54.0", "Linux");')
cur.execute('INSERT INTO assigned_websites VALUES (NULL, 1, 1);')
cur.execute('INSERT INTO assigned_websites VALUES (3, 0, 25);')
con.commit()

con.close()
