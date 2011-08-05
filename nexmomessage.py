import urllib
import urllib2
import urlparse
import json

class NexmoMessage:

    def __init__(self, details):
        self.sms = details
        if 'type' not in self.sms:
            self.sms['type'] = 'text'
        self.smstypes = [
            'text',
            'binary',
            'wappush',
            # todo: 'unicode', 'vcal', 'vcard'
        ]

    def url_fix(self, s, charset = 'utf-8'):
        if isinstance(s, unicode):
            s = s.encode(charset, 'ignore')
        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')
        qs = urllib.quote_plus(qs, ':&=')
        return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

    def set_text_info(self, text):
        # automatically transforms msg to text SMS
        self.sms['type'] = 'text'
        self.sms['text'] = text

    def set_bin_info(self, body, udh):
        # automatically transforms msg to binary SMS
        self.sms['type'] = 'binary'
        self.sms['body'] = body
        self.sms['udh'] = udh

    def set_wappush_info(self, title, url, validity = False):
        # automatically transforms msg to wappush SMS
        self.sms['type'] = 'wappush'
        self.sms['title'] = title
        self.sms['url'] = url
        self.sms['validity'] = validity

    def check_sms(self):
        """ http://www.nexmo.com/documentation/index.html#request """
        # mandatory parameters for all messages
        if ('server' not in self.sms or not self.sms['server']) or \
                ('username' not in self.sms or not self.sms['username']) or \
                ('password' not in self.sms or not self.sms['password']) or \
                ('from' not in self.sms or not self.sms['from']) or \
                ('to' not in self.sms or not self.sms['to']):
            return False
        # SMS logic, check Nexmo doc for details
        elif self.sms['type'] not in self.smstypes:
            return False
        elif self.sms['type'] == 'text' and ('text' not in self.sms or \
                not self.sms['text']):
            return False
        elif self.sms['type'] == 'binary' and ('body' not in self.sms or \
                not self.sms['body'] or 'body' not in self.sms or \
                not self.sms['udh']):
            return False
        elif self.sms['type'] == 'wappush' and ('title' not in self.sms or \
                not self.sms['title'] or 'url' not in self.sms or \
                not self.sms['url']):
            return False
        return True

    def build_request(self):
        # check SMS logic
        if self.check_sms():
            # basic request
            self.request = "%s?username=%s&password=%s&from=%s&to=%s&type=%s" % \
                (self.sms['server'], self.sms['username'],
                 self.sms['password'], self.sms['from'],
                 self.sms['to'], self.sms['type'])
            # text message
            if self.sms['type'] == 'text':
                self.request += "&text=%s" % self.sms['text']
            # binary message
            elif self.sms['type'] == 'binary':
                self.request += "&body=%s&udh=%s" % (self.sms['body'],
                    self.sms['udh'])
            # wappush message
            elif self.sms['type'] == 'wappush':
                self.request += "&title=%s&url=%s" % (self.sms['title'],
                    self.sms['url'])
                if self.sms['validity']:
                    self.request += "&validity=%s" % self.sms['validity']
            return self.request
        return False

    def get_details(self):
        return self.sms

    def send_request(self):
        if not self.build_request():
            return False
        # for the future (XML)
        if self.sms['server'] == 'http://rest.nexmo.com/sms/json':
            return self.send_request_json(self.request)

    def send_request_json(self, request):
        return json.load(urllib2.urlopen(self.url_fix(request)))

# EOF
