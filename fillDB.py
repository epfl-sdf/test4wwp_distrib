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
                + str(i) + ', "'+ row[3] + '", "' + row[1]+ '", "' + row[2] + '", "' + row[5] + '", "' + row[6] + '", ' + row[0] + ');\n'))
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

con.close()

