'''
Created on 2014. 3. 9.

@author: shallaa
'''
import re

class Detect:
    agent = 'etc'
    browser = 'etc'
    browser_version = 'etc'
    os = 'etc'
    os_version = 'etc'
    device = 'pc'
    
    def get_match(self, pattern, source, default=''):
        res = re.findall(pattern, source)
        
        if len(res) > 0:
            return res[0]
        else:
            return default
    
    def __init__(self, agent):
        self.agent = str(agent).lower()
        
        if self.agent == None or self.agent == '':
            raise 'No Agent.'
            return None
        
        if 'android' in self.agent:
            self.browser = 'android'
            self.os = 'android'
            
            if 'mobile' in self.agent:
                self.browser = self.browser + 'Tablet'
                self.device = 'tablet'
            else:
                self.device = 'mobile'
                
            self.os_version = self.get_match('android ([\d.]+)', self.agent, self.os_version)
            self.browser_version = self.get_match('version\/([\d.]+)', self.agent, self.browser_version)
        elif 'ipad' in self.agent or 'iphone' in self.agent:
            if 'ipad' in self.agent:
                self.device = 'tablet'
                self.browser = 'ipad'
                self.os = 'ipad'
            else:
                self.device = 'mobile'
                self.browser = 'iphone'
                self.os = 'iphone'
                
            self.os_version = self.get_match('os ([\d_]+)', self.agent, self.os_version)
            self.browser_version = self.get_match('version\/([\S]+)', self.agent, self.get_match('webkit\/([\d]+)', self.agent, self.browser_version))
        elif 'win' in self.agent:
            self.os = 'win'
            ver = 'windows nt '
            
            if ver + '5.1' in self.agent:
                self.os_version = 'xp'
            elif ver + '6.0' in self.agent:
                self.os_version = 'vista'
            elif ver + '6.1' in self.agent:
                self.os_version = '7'
            elif ver + '6.2' in self.agent:
                self.os_version = '8'
            elif ver + '6.3' in self.agent:
                self.os_version = '8.1'
        elif 'mac' in self.agent:
            self.os = 'mac'
            self.os_version = self.get_match('os x ([\d._]+)', self.agent, self.os_version)
        elif 'linux' in self.agent:
            self.os = 'linux'
        elif 'x11' in self.agent:
            self.os = 'unix'
            
        if 'msie' in self.agent or 'trident' in self.agent:
            self.browser = 'ie'
            
            if 'iemobile' in self.agent:
                self.os = 'winMobile'
            
            if 'msie' in self.agent:
                self.browser_version = self.get_match('msie ([\d]+)', self.agent, self.browser_version)
            else:
                self.browser_version = '11'
        elif 'chrome' in self.agent or 'crios' in self.agent:
            self.browser = 'chrome'
            
            if 'chrome' in self.agent:
                self.browser_version = self.get_match('chrome\/([\d]+)', self.agent, self.browser_version)
            else:
                self.browser_version = self.get_match('webkit\/([\d]+)', self.agent, self.browser_version)
        elif 'firefox' in self.agent:
            self.browser = 'firefox'
            self.browser_version = self.get_match('firefox\/([\d]+)', self.agent, self.browser_version)
        elif 'safari' in self.agent:
            self.browser = 'safari'
            self.browser_version = self.get_match('version\/([\d]+)', self.agent, self.browser_version)
        elif 'opera' in self.agent or 'opr' in self.agent:
            self.browser = 'opera'
            self.browser_version = self.get_match('version\/([\d]+)',self.agent, self.browser_version)
        elif 'naver' in self.agent:
            self.browser = 'naver'