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
    # (id, name, Jahia, WP, userview, password)
    cur.execute(('INSERT INTO websites VALUES(' 
                + str(i) + ', "'+ row[4] + '", "' + row[2]+ '", "' + row[3] + '", "' + row[6] + '", "' + row[7] + '");\n'))
    i += 1
con.commit()
credentials.close()
print('Websites (Credentials) OK')

# Inset browsers
browsers = open(path + 'browsers.csv')
reader = csv.reader(browsers)
# It has already an ID
next(browsers)
for row in reader:
    cur.execute('INSERT INTO browsers VALUES (' + row[0] + ', "' + row[1] + '", "' + row[2] + '", "' + row[3] + '");')
con.commit()
browsers.close()
print('Browsers OK')

# Insert Users
users = open(path + 'users.csv')
reader = csv.reader(users)
next(reader)
for row in reader:
    cur.execute('INSERT INTO users VALUES (' + row[0] + ', "' + row[2] + '", "' + row[1] + '");')
con.commit()
users.close()
print('Users OK')

# Create browers_sites
cur.execute(('INSERT INTO browsers_sites (browser_id, website_id)'
            +'SELECT browsers.id , websites.id FROM browsers CROSS JOIN websites;' 
            ))
con.commit()

con.close()
