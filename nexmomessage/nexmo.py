#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

try:
    import urllib
    import urllib2
    import urlparse
except ImportError:
    from urllib import parse as urllib
    from urllib import request as urllib2
    from urllib import parse as urlparse
    unicode = str

import json


class Nexmo(object):
    def __init__(self):
        self.RESTURL = "https://rest.nexmo.com"
        self.APIURL = "https://api.nexmo.com"

    def __send_request_json(self, request):
        req = urllib2.Request(url=request)
        req.add_header('Accept', 'application/json')
        try:
            response = urllib2.urlopen(req)
            assert response.code == 200
            data = response.read()
            return json.loads(data.decode('utf-8'))
        except ValueError:
            return False

    def __send_request_xml(self, request):
        return "XML request not implemented yet."

    def send_nexmo_request(self, nexmo_obj):
        if nexmo_obj['reqtype'] == 'json':
            return self.__send_request_json(nexmo_obj['request_uri'])
        elif nexmo_obj['reqtype'] == 'xml':
            return self.__send_request_xml(nexmo_obj['request_uri'])

    def get_url_rest(self):
        return self.RESTURL

    def get_url_api(self):
        return self.APIURL

    def send_request(self):
        pass


class NexmoMessage(Nexmo):
    def __init__(self, details):
        Nexmo.__init__(self)
        self.sms = details
        self.sms.setdefault('type', 'text')
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

    def set_text_info(self, text):
        # automatically transforms msg to text SMS
        self.sms['type'] = 'text'
        # if message have unicode symbols send as unicode
        try:
            text.decode('ascii')
        except:
            self.sms['type'] = 'unicode'
            if isinstance(text, unicode):
                text = text.encode('utf8')
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
        # mandatory parameters for all requests
        if not self.sms.get('api_key') or not self.sms.get('api_secret'):
            raise Exception("API key or secret not set")

        # API requests handling
        if self.sms['type'] in self.apireqs:
            if self.sms['type'] == 'balance' or self.sms['type'] == 'numbers':
                return True
            elif self.sms['type'] == 'pricing' and not self.sms.get('country'):
                raise Exception("Pricing needs counry")
            return True
        # SMS logic, check Nexmo doc for details
        elif self.sms['type'] not in self.smstypes:
            raise Exception("Unknown type")
        elif self.sms['type'] == 'text' and not self.sms.get('text'):
            raise Exception("text missing")
        elif self.sms['type'] == 'binary' and (not self.sms.get('body') or
                                               not self.sms.get('udh')):
            raise Exception("binary payload missing")
        elif self.sms['type'] == 'wappush' and (not self.sms.get('title') or
                                                not self.sms.get('url')):
            raise Exception("title or URL missing")
        elif self.sms['type'] == 'vcal' and not self.sms.get('vcal'):
            raise Exception("vcal data missing")
        elif self.sms['type'] == 'vcard' and not self.sms.get('vcard'):
            raise Exception("vcard data missing")
        elif not self.sms.get('from') or not self.sms.get('to'):
            raise Exception("From or to missing")
        return True

    def build_request(self):
        # check SMS logic
        if not self.check_sms():
            return False
        elif self.sms['type'] in self.apireqs:
            self.sms['url'] = self.get_url_rest()
            # developer API
            # balance
            if self.sms['type'] == 'balance':
                self.request = "%s/account/get-balance/%s/%s" \
                    % (self.sms['url'], self.sms['api_key'],
                       self.sms['api_secret'])
            # pricing
            elif self.sms['type'] == 'pricing':
                self.request = "%s/account/get-pricing/outbound/%s/%s/%s" \
                    % (self.sms['url'], self.sms['api_key'],
                       self.sms['api_secret'], self.sms['country'])
            # numbers
            elif self.sms['type'] == 'numbers':
                self.request = "%s/account/numbers/%s/%s" \
                    % (self.sms['url'], self.sms['api_key'],
                       self.sms['api_secret'])
            self.sms['request_uri'] = self.request
            return self.sms
        else:
            # standard requests
            if self.sms['reqtype'] not in self.reqtypes:
                raise Exception("Unknown reqtype")
            params = self.sms.copy()
            params.pop('reqtype')
            #params.pop('server')
            server = "%s/sms/%s" % (self.get_url_rest(), self.sms['reqtype'])
            self.request = server + "?" + urllib.urlencode(params)
            self.sms['request_uri'] = self.request
            return self.sms

    def send_request(self):
        return self.send_nexmo_request(self.build_request())

    def get_details(self):
        return self.sms


class NexmoCall(Nexmo):
    def __init__(self, details):
        Nexmo.__init__(self)
        self.call = details
        self.call.setdefault('type', 'call')
        self.call.setdefault('reqtype', 'json')

        self.reqtypes = [
            'json',
            'xml'
        ]

    def check_call(self):
        # mandatory parameters for all requests
        if not self.call.get('api_key') or not self.call.get('api_secret'):
            raise Exception("API key or secret not set")

        if (('answer_url' not in self.call) or
                (not self.call.get('answer_url'))):
            raise Exception('Answer URL not set')

        return True

    def build_request(self):
        # check call logic
        if not self.check_call():
            return False
        else:
            # standard requests
            params = self.call.copy()
            params.pop('reqtype')
            server = "%s/call/%s" % (self.get_url_rest(), self.call['reqtype'])
            self.request = server + "?" + urllib.urlencode(params)
            self.call['request_uri'] = self.request
            return self.call

    def send_request(self):
        return self.send_nexmo_request(self.build_request())

    def get_details(self):
        return self.call


class NexmoTTS(Nexmo):
    def __init__(self, details):
        Nexmo.__init__(self)
        self.tts = details
        self.tts.setdefault('type', 'tts')
        self.tts.setdefault('reqtype', 'json')

        self.reqtypes = [
            'json',
            'xml'
        ]

    def check_tts(self):
        # mandatory parameters for all requests
        if not self.tts.get('api_key') or not self.tts.get('api_secret'):
            raise Exception("API key or secret not set")

        if (('text' not in self.tts) or (not self.tts.get('text'))):
            raise Exception('Text not set')

        return True

    def build_request(self):
        # check TTS logic
        if not self.check_tts():
            return False
        else:
            # standard requests
            params = self.tts.copy()
            params.pop('reqtype')
            server = "%s/tts/%s" % (self.get_url_api(), self.tts['reqtype'])
            self.request = server + "?" + urllib.urlencode(params)
            self.tts['request_uri'] = self.request
            return self.tts

    def send_request(self):
        return self.send_nexmo_request(self.build_request())

    def get_details(self):
        return self.tts


class NexmoVerify(Nexmo):
    def __init__(self, details):
        Nexmo.__init__(self)
        self.verify = details
        self.verify.setdefault('type', 'verify')
        self.verify.setdefault('reqtype', 'json')

        self.verify_reqs = [
            'verify',
            'verify/check',
            'verify/search',
            'verify/control'
        ]

        self.reqtypes = [
            'json',
            'xml'
        ]

    def check_verify(self):
        # mandatory parameters for all requests
        if not self.verify.get('api_key') or not self.verify.get('api_secret'):
            raise Exception("API key or secret not set")

        # verify request
        if ((self.verify['type'] == 'verify')
            and (('number' not in self.verify)
                 or ('brand' not in self.verify)
                 or (not self.verify.get('number'))
                 or (not self.verify.get('brand')))):
            raise Exception('verify request: number and/or brand not set')

        # verify check
        if ((self.verify['type'] == 'verify/check')
            and (('code' not in self.verify)
                 or ('request_id' not in self.verify))):
            raise Exception('verify check: code and/or request_id not set')

        # verify search
        if ((self.verify['type'] == 'verify/search')
            and (('request_id' not in self.verify)
                 and ('request_ids' not in self.verify))):
            raise Exception('verify search: request_id(s) not set')

        # verify control
        # request_id cmd
        if ((self.verify['type'] == 'verify/control')
            and (('request_id' not in self.verify)
                 or ('cmd' not in self.verify))):
            raise Exception('verify control: request_id and cmd not set')

        return True

    def build_request(self):
        # check verify logic
        if not self.check_verify():
            return False
        else:
            # standard requests
            params = self.verify.copy()
            params.pop('reqtype')
            server = "%s/%s/%s" % (self.get_url_api(), self.verify['type'],
                                   self.verify['reqtype'])
            self.request = server + "?" + urllib.urlencode(params)
            self.verify['request_uri'] = self.request
            return self.verify

    def send_request(self):
        return self.send_nexmo_request(self.build_request())

    def get_details(self):
        return self.verify


class NexmoNI(Nexmo):
    def __init__(self, details):
        Nexmo.__init__(self)
        self.ni = details
        self.ni.setdefault('type', 'ni')
        self.ni.setdefault('reqtype', 'json')

        self.reqtypes = [
            'json',
            'xml'
        ]

    def check_ni(self):
        # mandatory parameters for all requests
        if not self.ni.get('api_key') or not self.ni.get('api_secret'):
            raise Exception("ni: API key or secret not set")

        # ni request
        if ((self.ni['type'] == 'ni')
            and (('number' not in self.ni)
                 or ('callback' not in self.ni))):
            raise Exception('ni request: number and/or callback not set')

        return True

    def build_request(self):
        # check ni logic
        if not self.check_ni():
            return False
        else:
            # standard requests
            params = self.ni.copy()
            params.pop('reqtype')
            server = "%s/%s/%s" % (self.get_url_rest(), self.ni['type'],
                                   self.ni['reqtype'])
            self.request = server + "?" + urllib.urlencode(params)
            self.ni['request_uri'] = self.request
            return self.ni

    def send_request(self):
        return self.send_nexmo_request(self.build_request())

    def get_details(self):
        return self.ni
