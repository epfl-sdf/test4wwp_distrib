import web
from web import form
import time
from random import randint
import datetime
import re
import base64

from distrib_credentials import distrib_allowed

render = web.template.render('Templates/')

urls = (
	'/', 'index',
	'/sites', 'sites',
	'/compare', 'compare',
	'/next', 'next',
    '/login', 'login'
)

db = web.database(dbn='sqlite', db='python.db')
names = db.query('SELECT ID, NAME FROM users').list()
status = ['DONE', 'BUSY', 'EMPTY', 'CONNECTION ERROR', None]

button = form.Form(
    form.Button("submit", type="submit", description="Next"),
)

class login:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ','',auth)
            username,password = base64.decodestring(auth).split(':')
            if (username,password) in distrib_allowed:
                raise web.seeother('/')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate','Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return

class index:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is None:
            raise web.seeother('/login')
        return render.index(names)

class sites:
    def GET(self):
        sites = db.query("SELECT * FROM sites;").list()
        if web.ctx.env.get('HTTP_AUTHORIZATION') is None:
            raise web.seeother('/login')
        for site in sites:
            if site.DATE:
                site.DATE =datetime.datetime.fromtimestamp(int(site.DATE)).strftime('%Y-%m-%d %H:%M:%S')	
            return render.sites(sites, names, status)

class compare:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is None:
            raise web.seeother('/login')
        url1 = web.input(url1=None).url1
        url2 = web.input(url2=None).url2
        user_id = web.input(user_id = None).user_id
        if user_id:
            if (int(user_id) <= 0) or (int(user_id) > len(names)):
                raise web.seeother('/')
        if url1 and url2:
            return render.compare(names, user_id, status, url1, url2)
        else:
            urls = db.query('SELECT JAHIA, WORDPRESS FROM sites WHERE STATUS="BUSY" AND USER_ID="' + user_id + '";').list()
     	    if not urls:
		        urls = db.query('SELECT JAHIA, WORDPRESS FROM sites WHERE STATUS IS NULL;').list()
        if not urls:
            return "No more sites to compare"
        rdm_id = randint(0, len(urls)-1)
        temp = urls[rdm_id]
        if (db.query('SELECT STATUS FROM sites WHERE JAHIA="' + temp.JAHIA + '"')!='DONE'):
            db.update('sites', where='JAHIA="' + temp.JAHIA + '"', STATUS='BUSY', USER_ID=user_id, DATE=time.time())
        raise web.seeother('/compare?user_id=' + user_id + '&url1=' + temp.JAHIA + '&url2=' + temp.WORDPRESS)

    def POST(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is None:
            raise web.seeother('/login')
        user_id = web.input(select=None).select
        if user_id != "empty":
            raise web.seeother('/compare?user_id=' + user_id)
        else:
            raise web.seeother('/')



class next:
    def POST(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is None:
            raise web.seeother('/login')
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
