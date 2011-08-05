import urllib
import urllib2
import urlparse
import json

class NexmoMessage:

    def __init__(self, s, u, p, f = False, t = False, m = False, ty = "text",
            st = False, cl = False, nt = False, vr = False, vl = False,
            bo = False, ud = False):
        self.sms = {'server': s, 'username': u, 'password': p, 'sender': f,
                    'recipient': t, 'message': m, 'type': ty,
                    'status-report-req': st, 'client-ref': cl,
                    'network-code': nt, 'vcard': vr, 'vcal': vl, 'body': bo,
                    'udh': ud }
        self.smstypes = [
            'text',
            'binary',
            # todo: 'wappush', 'unicode', 'vcal', 'vcard'
        ]

    def urlFix(self, s, charset = 'utf-8'):
        if isinstance(s, unicode):
            s = s.encode(charset, 'ignore')
        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')
        qs = urllib.quote_plus(qs, ':&=')
        return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

    def setTextInfo(self, m):
        # automatically transforms msg to text SMS
        self.sms['type'] = 'text'
        self.sms['message'] = m

    def setBinInfo(self, b, u):
        # automatically transforms msg to binary SMS
        self.sms['type'] = 'binary'
        self.sms['body'] = b
        self.sms['udh'] = u

    def checkSMS(self):
        """ http://www.nexmo.com/documentation/index.html#request """
        # mandatory parameters
        if not self.sms['server'] or not self.sms['username'] or \
               not self.sms['password'] or not self.sms['sender'] or \
               not self.sms['recipient']:
            return False
        # SMS logic, check Nexmo doc for details
        if self.sms['type'] not in self.smstypes:
            return False
        if self.sms['type'] == 'text' and not self.sms['message']:
            return False
        if self.sms['type'] == 'binary' and (not self.sms['body'] or \
                not self.sms['udh']):
            return False
        if self.sms['type'] == 'vcard' and not self.sms['vcard']:
            return False
        if self.sms['type'] == 'vcal' and not self.sms['vcal']:
            return False
        return True

    def buildRequest(self):
        # check SMS logic
        if self.checkSMS():
            # basic request
            self.request = "%s?username=%s&password=%s&from=%s&to=%s&type=%s" % \
                (self.sms['server'], self.sms['username'],
                 self.sms['password'], self.sms['sender'],
                 self.sms['recipient'], self.sms['type'])
            # text message
            if self.sms['type'] == 'text':
                self.request += "&text=%s" % self.sms['message']
            # binary message
            if self.sms['type'] == 'binary':
                self.request += "&body=%s&udh=%s" % (self.sms['body'],
                    self.sms['udh'])
            return self.request
        return False

    def getDetails(self):
        return self.sms

    def sendRequest(self):
        if not self.buildRequest():
            return False
        # for the future (XML)
        if self.sms['server'] == 'http://rest.nexmo.com/sms/json':
            return self.sendRequestJson(self.request)

    def sendRequestJson(self, r):
        return json.load(urllib2.urlopen(self.urlFix(r)))

# EOF
