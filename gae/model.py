'''
Created on 2014. 2. 6.

@author: shallaa
'''

from google.appengine.ext import db

class Ligo(db.Model):
    link = db.URLProperty()
    ligo = db.StringProperty()
    date = db.DateTimeProperty(auto_now=True)
    hit  = db.IntegerProperty(default=0)
    
    def __unicode__(self):
        return 'ligo: %s, link: %s'%(self.ligo, self.link)
    
class WebLog(db.Model):
    browser     = db.StringProperty()
    browser_ver = db.StringProperty()
    os          = db.StringProperty()
    os_ver      = db.StringProperty() 
    device      = db.StringProperty()
    referer     = db.StringProperty()
    language    = db.StringProperty()
    agent       = db.StringProperty()
    date        = db.DateTimeProperty(auto_now_add=True)
    
    def __unicode__(self):
        return 'agent: %s'%(self.agent)
    
class AppLog(db.Model):
    log  = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
    def __unicode__(self):
        return 'log %s'%(self.log)