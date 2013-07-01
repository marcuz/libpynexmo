#
# Copyright (c) 2013 Marco Londero <marco.londero@linux.it>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import urllib
import urllib2
import urlparse
import json

BASEURL = "https://rest.nexmo.com"


class NexmoMessage:

    def __init__(self, details):
        self.sms = details
        self.sms.setdefault('type', 'text')
        self.sms.setdefault('server', BASEURL)
        self.sms.setdefault('reqtype', 'json')

        self.smstypes = [
            'text',
            'binary',
            'wappush',
            'vcal',
            'vcard',
            'unicode'
        ]
        self.apireqs = [
            'balance',
            'pricing',
            'numbers'
        ]
        self.reqtypes = [
            'json',
            'xml'
        ]

    def url_fix(self, s, charset='utf-8'):
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

    def set_wappush_info(self, title, url, validity=False):
        # automatically transforms msg to wappush SMS
        self.sms['type'] = 'wappush'
        self.sms['title'] = title
        self.sms['url'] = url
        self.sms['validity'] = validity

    def set_vcal_info(self, vcal):
        # automatically transforms msg to vcal SMS
        self.sms['type'] = 'vcal'
        self.sms['vcal'] = vcal

    def set_vcard_info(self, vcard):
        # automatically transforms msg to vcard SMS
        self.sms['type'] = 'vcard'
        self.sms['vcard'] = vcard

    def check_sms(self):
        """ http://www.nexmo.com/documentation/index.html#request
            http://www.nexmo.com/documentation/api/ """
        # mandatory parameters for all requests
        if not self.sms.get('api_key') or not self.sms.get('api_secret'):
            return False

        # API requests handling
        if self.sms['type'] in self.apireqs:
            if self.sms['type'] == 'balance' or self.sms['type'] == 'numbers':
                return True
            elif self.sms['type'] == 'pricing' and not self.sms.get('country'):
                return False
            return True
        # SMS logic, check Nexmo doc for details
        elif self.sms['type'] not in self.smstypes:
            return False
        elif self.sms['type'] == 'text' and not self.sms.get('text'):
            return False
        elif self.sms['type'] == 'binary' and (not self.sms.get('body') or
                                               not self.sms.get('udh')):
            return False
        elif self.sms['type'] == 'wappush' and (not self.sms.get('title') or
                                                not self.sms.get('url')):
            return False
        elif self.sms['type'] == 'vcal' and not self.sms.get('vcal'):
            return False
        elif self.sms['type'] == 'vcard' and not self.sms.get('vcard'):
            return False
        elif not self.sms.get('from') or not self.sms.get('to'):
            return False
        return True

    def build_request(self):
        # check SMS logic
        if not self.check_sms():
            return False
        elif self.sms['type'] in self.apireqs:
            # basic API requests
            # balance
            if self.sms['type'] == 'balance':
                self.request = "%s/account/get-balance/%s/%s" % (BASEURL,
                               self.sms['api_key'], self.sms['api_secret'])
            # pricing
            elif self.sms['type'] == 'pricing':
                self.request = "%s/account/get-pricing/outbound/%s/%s/%s" \
                    % (BASEURL, self.sms['api_key'], self.sms['api_secret'],
                       self.sms['country'])
            # numbers
            elif self.sms['type'] == 'numbers':
                self.request = "%s/account/numbers/%s/%s" % (BASEURL,
                               self.sms['api_key'], self.sms['api_secret'])
            return self.request
        else:
            # standard requests
            if self.sms['reqtype'] not in self.reqtypes:
                return False
            params = self.sms.copy()
            params.pop('reqtype')
            params.pop('server')
            server = "%s/sms/%s" % (BASEURL, self.sms['reqtype'])
            self.request = server + "?" + urllib.urlencode(params)
            return self.request
        return False

    def get_details(self):
        return self.sms

    def send_request(self):
        if not self.build_request():
            return False
        if self.sms['reqtype'] == 'json':
            return self.send_request_json(self.request)
        elif self.sms['reqtype'] == 'xml':
            return self.send_request_xml(self.request)

    def send_request_json(self, request):
        url = request
        req = urllib2.Request(url=url)
        req.add_header('Accept', 'application/json')
        try:
            return json.load(urllib2.urlopen(req))
        except ValueError:
            return False

    def send_request_xml(self, request):
        return "XML request not implemented yet."
