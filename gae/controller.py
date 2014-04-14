'''
Created on 2014. 2. 5.

@author: shallaa
'''
# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2
import random
from model import Ligo, WebLog, AppLog
from detect import Detect
from google.appengine.api import urlfetch
from google.appengine.api.urlfetch_errors import SSLCertificateError, ResponseTooLargeError, DownloadError, DeadlineExceededError, InvalidURLError, InvalidMethodError

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

ligoKeys = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

allowDomains = ('topuit.naver.com', 'nhncorp.com')
DOMAIN = 'ligo.kr'

def insertLog(log):
    try:
        applog = AppLog()
        applog.log = str(log)
        applog.put()
    except Exception, e:
        print(e)
        return

def insertWebLog(request):
    referer  = 'etc'
    language = 'etc'
    agent    = 'etc'
    
    try:
        referer = str(request.referer)
    except Exception, e:
        insertLog(e)
        
    try:
        language = str(request.accept_language)
    except Exception, e:
        insertLog(e)
        
    try:
        agent = str(request.user_agent).lower()
    except Exception, e:
        insertLog(e)
    
    try:
        detect = Detect(agent)
    except Exception, e:
        insertLog(e)
        return
    
    try:        
        weblog = WebLog()
        weblog.browser     = detect.browser
        weblog.browser_ver = detect.browser_version
        weblog.os          = detect.os
        weblog.os_ver      = detect.os_version
        weblog.device      = detect.device
        weblog.referer     = referer
        weblog.language    = language
        weblog.agent       = agent
        weblog.put()
    except Exception, e:
        insertLog(e)

def doRender(handler, tname='index.html', values={}, allow=False):
    newval = dict(values)
    outstr = JINJA_ENVIRONMENT.get_template(tname).render(newval)
    
    if allow == True:
        handler.response.headers.add_header('Access-Control-Allow-Origin', '*')
        handler.response.headers.add_header('Access-Control-Allow-Credentials', 'true')

    handler.response.out.write(outstr)
    
    return True

def doRenderJsonP(handler, callback, data):
    newval = dict({'callback':callback, 'data':data})
    outstr = JINJA_ENVIRONMENT.get_template('jsonp.html').render(newval)

    handler.response.headers['Content-Type'] = 'application/javascript; charset=UTF-8'
    handler.response.out.write(outstr)

    return True

def createLigo(count):
    key = []
    
    for i in range(count):
        i = random.randrange(0, 36)
        
        if i < 26:
            key.insert(0, ligoKeys[i])
        else:
            key.append(ligoKeys[i])
        
    return ''.join(key)

def fetchLink(link):
    try:
        urlfetch.fetch(link)
    except InvalidMethodError, e:
        insertLog(e)
        
        return 'Invalid value for method.'
    except SSLCertificateError, e:
        insertLog(e)
        
        return 'Invalid server certificate.'
    except ResponseTooLargeError, e:
        insertLog(e)
        
        return 'Response was too large and was truncated.'
    except DownloadError, e:
        insertLog(e)
        
        return 'Could not contact the server.'
    except DeadlineExceededError, e:
        insertLog(e)
        
        return 'Deadline was exceeded.'
    except InvalidURLError, e:
        insertLog(e)
        
        return 'URL given is empty or invalid'
    except Exception, e:
        insertLog(e)
        
        return 'Unknown error'
        
    return 'ok'

def insertLink(url):
    if url == None or url == '' or url == 'null':
        insertLog('Link is Empty')
        return 'Enter the URL.'
    
    if DOMAIN in url:
        insertLog('Already shortened URL')
        return 'Already shortened URL'
    
    allow = False
    
    for domain in allowDomains:
        if domain in url:
            allow = True
            break
    
    if not url.startswith('http'):
        url = 'http://' + url

    res_fetch = fetchLink(url)
        
    if res_fetch != 'ok':
        if allow != True:
            return res_fetch
     
    if url.endswith('/'):
        url = url[:-1]
        
    entity = Ligo.get_or_insert(url)
    
    if entity.link is None:
        entity.link = url
            
    if entity.ligo is None:
        count = 2
        num = 0
        
        while True:
            ligoKey = createLigo(count)
            
            try:
                res = Ligo.all().filter('ligo = ', ligoKey).fetch(limit=1)
            except Exception, e:
                insertLog(e)
                return e
            
            if len(res) < 1:
                entity.ligo = ligoKey
                break
            else:
                num = num + 1
            
            if num > 1:
                count = count + 1
                num = 0
                
    entity.hit = entity.hit + 1
    entity.put()
    
    return 'http://' + DOMAIN + '/' + entity.ligo

class MainHandler(webapp2.RequestHandler):
    def get(self):
        url = str(self.request.url)

        insertWebLog(self.request)
        
        if url.startswith('http://api.'):
            try:
                url = str(self.request.get('url')).strip()
            except Exception, e:
                insertLog(e)
                doRender(self, 'result.html', {'res':'Invalid string.'})
                return
            
            doRender(self, 'result.html', {'res':insertLink(url)}, True)
            return
        
        if url.startswith('http://jsonp.'):
            try:
                url = str(self.request.get('url')).strip()
                callback = str(self.request.get('callback')).strip()
            except Exception, e:
                insertLog(e)
                doRenderJsonP(self, callback, 'Invalid string.')
                return

            doRenderJsonP(self, callback, insertLink(url))
            return;
            
        try:
            linkKey = str(self.request.path)
        except Exception, e:
            insertLog(e)
            doRender(self, "index.html")
        
        if linkKey.startswith('/'):
            linkKey = linkKey[1:]
        
        try:
            res = Ligo.all().filter('ligo =', linkKey).fetch(limit=1)
        except Exception, e:
            insertLog(e)
            res = []
        
        for ligo in res:
            ligo.hit = ligo.hit + 1
            ligo.put()
            
            self.redirect(str(ligo.link))
            doRender(self, 'result.html', {'res':''})
            return
        
        doRender(self, 'index.html')
        
    def post(self):
        if self.request.url in self.request.headers['Referer'] == False:
            doRender(self, 'result.html', {'res':'Wrong approach.'})
            return
        
        try:
            url = str(self.request.get('url')).strip()
        except Exception, e:
            insertLog(e)
            doRender(self, 'result.html', {'res':'Invalid string.'})
            return
        
        doRender(self, 'result.html', {'res':insertLink(url)})
        
app = webapp2.WSGIApplication([('/.*', MainHandler)])