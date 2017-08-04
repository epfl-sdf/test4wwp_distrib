import web
from web import form
import time
from random import randint
import datetime
import httpagentparser

print('\n')
print('   ---------------------------')
print('   | Distrib Version : 1.1.0 |')
print('   ---------------------------')
print('\n')

render = web.template.render('Templates/')

urls = (
	'/', 'index',
	'/logs', 'logs',
	'/compare', 'compare',
	'/next', 'next'
)


db = web.database(dbn='sqlite', db='../credentials/distrib.db')
names = db.query('SELECT id, first_name, last_name FROM users').list()
status = ['DONE', 'STARTED', 'EMPTY', 'CONNECTION ERROR', None]

button = form.Form(
    form.Button("submit", type="submit", description="Next"),
)

class query:
    @staticmethod
    def get_url(user_id, browser_info):
        # search for 'started' site
	urls = db.query(('SELECT s.id, s.jahia, s.wordpress, l.status '
                        +'FROM logs l INNER JOIN browsers b ON l.browser_id = b.id '
                        +'INNER JOIN websites s ON l.website_id = s.id '
                        +'WHERE l.user_id = ' + user_id 
                        +' AND b.name = "' + browser_info['browser']['name'] + '"' 
                        +' AND b.os = "' + browser_info['platform']['name'] + '"'
                        +'ORDER BY l.date DESC LIMIT 1;')).list()
        # if 'started' site
        if urls: 
            if urls[0].status == 'STARTED':
                return urls[0]
            else:
                urls = None
        # if no 'started' site
        if not urls:
	    urls = db.query(('SELECT w.id, jahia, wordpress FROM '
                            + '(logs INNER JOIN websites w ON NOT logs.website_id = w.id INNER JOIN browsers b)'
                            + ' WHERE NOT (b.name = "' + browser_info['browser']['name'] + '"' 
                            + ' AND b.os = "' + browser_info['platform']['name'] + '");')).list()
        # if logs is empty
        if not urls:
            urls = db.query('SELECT id, jahia, wordpress FROM websites;').list()
        rdm_id = randint(0, len(urls)-1)
        url = urls[rdm_id]
        url.status = None
        return url
    
    @staticmethod
    def get_browser_id(browser_info):
        browser_id = db.query(( 'SELECT id FROM browsers b '
                        +'WHERE b.name = "' + browser_info['browser']['name'] + '" '
                        +'AND b.version = "' + browser_info['browser']['version'] + '"'
                        +'AND b.os = "' + browser_info['platform']['name'] + '";'
                    )).list()
        if browser_id:
            return browser_id[0].id
        else:
            return None

    @staticmethod
    def add_browser(browser_info):
        return db.insert('browsers', name = browser_info['browser']['name'], 
                version = browser_info['browser']['version'], os = browser_info['platform']['name'])
    
    @staticmethod
    def add_log(user_id, browser_id, website_id, status):
        db.insert('logs', user_id = user_id, browser_id = browser_id, website_id = website_id, date = time.time(), status = status)

    @staticmethod
    def get_id_from_jahia_url(jahia):
        return db.query('SELECT id FROM websites WHERE jahia = "' + jahia + '";').list()[0].id

class index:
    def GET(self):
        return render.index(names)

class logs:
	def GET(self):
		logs = db.query("SELECT s.jahia, s.wordpress, b.os, b.name, l.date, u.first_name, u.last_name, l.status FROM logs l INNER JOIN browsers b ON l.browser_id=b.id INNER JOIN users u ON l.user_id=u.id INNER JOIN websites s ON l.website_id=s.id ORDER BY l.date DESC;").list()
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
            url = query.get_url(user_id, browser_info)
	    if not url:
                return "No more sites to compare"
        if not url.status:
            query.add_log(user_id, browser_id, url.id, 'STARTED')
        raise web.seeother('/compare?user_id=' + user_id + '&url1=' + url.jahia + '&url2=' + url.wordpress)

    def POST(self):
        user_id = web.input(select=None).select
        if user_id != "empty":
            raise web.seeother('/compare?user_id=' + user_id)
        else:
            raise web.seeother('/')



class next:
    def POST(self):
        statu = web.input(select = None).select
        if statu:
            browser_info =  httpagentparser.detect(web.ctx.env.get('HTTP_USER_AGENT'))
            browser_id = query.get_browser_id(browser_info)
            url = web.input(url1=None).url1
            user_id = web.input(user_id=None).user_id
            if user_id != '0':
                query.add_log(user_id, browser_id, query.get_id_from_jahia_url(url), statu)
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
