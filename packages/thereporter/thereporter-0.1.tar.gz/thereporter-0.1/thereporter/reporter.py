import requests

NOTSET = 0
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50
_header = {NOTSET:'',DEBUG:'🐛DEBUG🐛\n',INFO:'ℹINFOℹ\n',WARNING:'⚠WARNING⚠',ERROR:'🚫ERROR🚫\n',CRITICAL:'🚨CRITICAL🚨\n'}

class Reporter:
    
    def __init__(self, token: str, url: str = 'http://54.93.165.224:5000/report'):
        self.url = url
        self.token = token
        
    def report(self, message: str, level:int = NOTSET):
        params = {'token':self.token,'message':_header[level]+message}
        requests.post(url = self.url, params = params)
        