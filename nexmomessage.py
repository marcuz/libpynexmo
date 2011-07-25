import urllib
import urllib2
import urlparse
import json

SMS_CHARS = 160

class NexmoMessage:
    def __init__(self, s, u, p):
        self.apiserver = s
        self.apiuser = u
        self.apipass = p

    def urlFix(self, s, charset = 'utf-8'):
        if isinstance(s, unicode):
            s = s.encode(charset, 'ignore')
        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')
        qs = urllib.quote_plus(qs, ':&=')
        return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

    def textMessage(self, f, t, m):
        self.apifrom = f
        self.apito = t
        self.apimsg = m
        self.request = "%s?username=%s&password=%s&from=%s&to=%s&text=%s" % (self.apiserver, self.apiuser, self.apipass, self.apifrom, self.apito, self.apimsg) 

    def sendRequest(self):
        print json.load(urllib2.urlopen(self.urlFix(self.request)))

# EOF
