import web
import time
import datetime
import httpagentparser

from operator import itemgetter
from web import form
from random import randint
from version import __version__

print('\n')
print('   ---------------------------')
print('   | Distrib Version : ' +__version__+' |')
print('   ---------------------------')
print('\n')

render = web.template.render('Templates/')

urls = (
	'/', 'index',
	'/logs', 'logs',
	'/compare', 'compare',
	'/assigned', 'assigned',
	'/next', 'next'
)


db = web.database(dbn='sqlite', db='../credentials/distrib.db')
names_orderN = db.query('SELECT id, first_name, last_name FROM users ORDER BY first_name').list()
names = db.query('SELECT id, first_name, last_name FROM users').list()
names = sorted(names, key=itemgetter('first_name'))
status = ['DONE', 'STARTED', 'EMPTY', 'CONNECTION ERROR', None]

button = form.Form(
    form.Button("submit", type="submit", description="Next"),
)

class query:
    @staticmethod
    def get_url(user_id, browser_id):
        if browser_id and user_id:
            url = None
            urls = None
            empty_logs = query.is_logs_empty()

            if not empty_logs:
                # search for 'STARTED' site
	        urls = db.query(('SELECT w.id, w.jahia, w.wordpress, l.status, MAX(l.date) FROM websites w '
                                +'INNER JOIN logs l ' 
                                +'ON (w.id = l.website_id '
                                +    ' AND l.user_id = ' + str(user_id)  
                                +    ' AND l.browser_id = ' + str(browser_id) + ');')).list()
                # if 'STARTED' site
                if urls: 
                    # There was logs for this user and this browser
                    if urls[0].status == 'STARTED':
                        return urls[0]
                    else:
                        urls = None
    
                # if no 'STARTED' site
                if not urls:
                    urls = db.query(('SELECT w.id, w.jahia, w.wordpress FROM websites w LEFT JOIN '
                                    +'(SELECT done.website_id FROM ' 
                                    +'(browsers b  INNER JOIN logs l '
                                    +'ON (b.id = l.browser_id AND ' + str(browser_id) + ' = l.browser_id)) as done) '
                                    +'ON (website_id =  w.id) '
                                    +'WHERE website_id IS NULL '
                                    +'ORDER BY w.random;')).list()
                                    
            # if logs is empty 
            if not urls and empty_logs:
                urls = db.query('SELECT id, jahia, wordpress, MIN(random) FROM websites;').list()
            if urls:
                url = urls[0]
                url.status = None
            return url

    @staticmethod
    def is_logs_empty():
        logs = db.query('SELECT date FROM logs LIMIT 1;')
        return (logs is None)
    
    @staticmethod
    def get_browser_id(browser_info):
        browser_id = db.query(( 'SELECT id FROM browsers b '
                        +'WHERE b.name = "' + browser_info['browser']['name'] + '" '
                        +'AND b.os = "' + browser_info['platform']['name'] + '";'
                    )).list()
        if browser_id:
            return browser_id[0].id
        else:
            return None

    @staticmethod
    def get_assigned_url(user_id, browser_id):
        url = db.query(('SELECT id, jahia, wordpress FROM '
                        +'(SELECT * FROM assigned_websites aw '
                        +'WHERE (aw.browser_id = ' + str(browser_id)  
                        + ' AND aw.user_id = ' + str(user_id) + ')) as aw '
                        +'INNER JOIN websites w '
                        +'ON (w.id = aw.website_id) LIMIT 1;')).list()
        if not url:
            url = db.query(('SELECT id, jahia, wordpress FROM '
                        +'(SELECT * FROM assigned_websites aw '
                        +'WHERE (aw.user_id IS NULL AND aw.browser_id = ' + str(browser_id) + ')) as aw '
                        +'INNER JOIN websites w '
                        +'ON (w.id = aw.website_id) LIMIT 1;')).list()
        if url:
            url = url[0]
            url.status = None
            return url
        else:
            return None 

    @staticmethod
    def update_assigned_websites(website_id, browser_id):
	db.delete('assigned_websites', where='browser_id=' + str(browser_id) + ' AND website_id=' + str(website_id) )	

    @staticmethod
    def add_browser(browser_info):
        return db.insert('browsers', name = browser_info['browser']['name'], 
                version = 0, os = browser_info['platform']['name'])
    
    @staticmethod
    def add_log(user_id, browser_id, website_id, status):
        db.insert('logs', user_id = user_id, browser_id = browser_id, website_id = website_id, date = time.time(), status = status)

    @staticmethod
    def get_id_from_jahia_url(jahia):
        return db.query('SELECT id FROM websites WHERE jahia = "' + jahia + '";').list()[0].id

class index:
    def GET(self):
        return render.index(names_orderN, __version__)

class logs:
	def GET(self):
		logs = db.query('SELECT * FROM full_logs').list()
		for log in logs:
			if log.date:
				log.date = datetime.datetime.fromtimestamp(int(log.date)).strftime('%Y-%m-%d %H:%M:%S')	
		return render.logs(logs)

class compare:
    def GET(self):
        url1 = web.input(url1=None).url1
        url2 = web.input(url2=None).url2
        user_id = web.input(user_id = None).user_id
        if user_id:
            if (int(user_id) <= 0) or (int(user_id) > len(names)):
                raise web.seeother('/')
        if url1 and url2:
            return render.compare(names, user_id, status, url1, url2)
        else:
	    browser_info = httpagentparser.detect(web.ctx.env.get('HTTP_USER_AGENT'))
            browser_id = query.get_browser_id(browser_info)
            if not browser_id:
                browser_id = query.add_browser(browser_info)
            url = query.get_assigned_url(user_id, browser_id)
            if not url:
                url = query.get_url(user_id, browser_id)
	    if not url:
                return "No more sites to compare"
        if not url.status:
            print(query.add_log(user_id, browser_id, url.id, 'STARTED'))
        raise web.seeother('/compare?user_id=' + user_id + '&url1=' + url.jahia + '&url2=' + url.wordpress)

    def POST(self):
        user_id = web.input(select=None).select
        if user_id != "empty":
            raise web.seeother('/compare?user_id=' + user_id)
        else:
            raise web.seeother('/')

class assigned:
    def GET(self):
        browsers = db.query('SELECT * FROM browsers;').list()
        websites = db.query('SELECT id, jahia, wordpress FROM websites;').list()
        assigneds = db.query('SELECT * FROM assigned_websites;').list()

        return render.assigned(assigneds, names, browsers, websites)

class next:
    def POST(self):
        statu = web.input(select = None).select
        if statu:
            browser_info =  httpagentparser.detect(web.ctx.env.get('HTTP_USER_AGENT'))
            browser_id = query.get_browser_id(browser_info)
            url = web.input(url1=None).url1
            user_id = web.input(user_id=None).user_id
            if user_id != '0':
		website_id = query.get_id_from_jahia_url(url)
		query.update_assigned_websites(website_id, browser_id)
                query.add_log(user_id, browser_id, website_id, statu)
                raise web.seeother('/compare?user_id=' + user_id)
            else:
                raise web.seeother('/')

        else:
            url1 = web.input(url1=None).url1
            url2 = web.input(url2=None).url2
            user_id = web.input(user_id = None).user_id
            if user_id:
                if (int(user_id) <= 0) or (int(user_id) > len(names)):
                    raise web.seeother('/')
            if url1 and url2:
                return render.compare(names, user_id, status, url1, url2)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
