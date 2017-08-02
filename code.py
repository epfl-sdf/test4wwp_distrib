import web
from web import form
import time
from random import randint
import datetime
import httpagentparser

render = web.template.render('Templates/')

urls = (
	'/', 'index',
	'/sites', 'sites',
	'/compare', 'compare',
	'/next', 'next'
)


db = web.database(dbn='sqlite', db='../credentials/distrib.db')
names = db.query('SELECT id, first_name, last_name FROM users').list()
status = ['DONE', 'BUSY', 'EMPTY', 'CONNECTION ERROR', None]

button = form.Form(
    form.Button("submit", type="submit", description="Next"),
)

class query:
    @staticmethod
    def get_urls(user_id, browser_info):
	urls = db.query(('SELECT s.jahia, s.wordpress '
                        +'FROM logs l INNER JOIN browsers b ON l.browser_id = b.id '
                        +'INNER JOIN websites s ON l.website_id = s.id '
                        +'WHERE l.user_id = ' + user_id 
                        +' AND b.name = "' + browser_info['browser']['name'] + '"' 
                        +' AND b.os = "' + browser_info['platform']['name'] + '"'
                        +' AND l.status = "BUSY" '
                        +'ORDER BY date(date) DESC Limit 1;')).list()
        if not urls:
	    urls = db.query('SELECT jahia, wordpress FROM websites WHERE STATUS IS NULL;').list()
        return urls


class index:
    def GET(self):
        return render.index(names)

class sites:
	def GET(self):
		sites = db.query("SELECT * FROM sites;").list()
		for site in sites:
			if site.DATE:
				site.DATE =datetime.datetime.fromtimestamp(int(site.DATE)).strftime('%Y-%m-%d %H:%M:%S')	
		return render.sites(sites, names, status)

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
	    browser_info =  httpagentparser.detect(web.ctx.env.get('HTTP_USER_AGENT'))
            print('--------------------------------\n')
            print(browser_info)
            urls = query.get_urls(user_id, browser_info)
	    if not urls:
                return "No more sites to compare"
        rdm_id = randint(0, len(urls)-1)
        temp = urls[rdm_id]
        if (db.query('SELECT STATUS FROM sites WHERE JAHIA="' + temp.JAHIA + '"')!='DONE'):
            db.update('sites', where='JAHIA="' + temp.JAHIA + '"', STATUS='BUSY', USER_ID=user_id, DATE=time.time())
        raise web.seeother('/compare?user_id=' + user_id + '&url1=' + temp.JAHIA + '&url2=' + temp.WORDPRESS)

    def POST(self):
        user_id = web.input(select=None).select
        if user_id != "empty":
            raise web.seeother('/compare?user_id=' + user_id)
        else:
            raise web.seeother('/')



class next:
    def POST(self):
        statu = web.input(select = None).select
        print(statu)
        if statu:
            update_status(statu)
        else:
            url1 = web.input(url1=None).url1
            url2 = web.input(url2=None).url2
            user_id = web.input(user_id = None).user_id
            if user_id:
                if (int(user_id) <= 0) or (int(user_id) > len(names)):
                    raise web.seeother('/')
            if url1 and url2:
                return render.compare(names, user_id, status, url1, url2)

def update_status(status):
    url = web.input(url1=None).url1
    user_id = web.input(user_id=0).user_id
    if user_id != '0':
        db.update('sites', where='JAHIA="' + url + '"', STATUS=status, DATE=time.time())
        raise web.seeother('/compare?user_id=' + user_id)
    else:
        raise web.seeother('/')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
