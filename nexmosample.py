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

import sys

from nexmomessage import NexmoMessage


def main():

    r = "json"
    u = "changeme"
    p = "changeme"
    f = "marcuz"
    t = "39**********"
    m = "fool the reader àèìòù !!!"

    msg = {'reqtype': r, 'api_secret': p, 'from': f, 'to': t, 'api_key': u}

    # account balance
    req = {'api_secret': p, 'api_key': u, 'type': 'balance'}
    print("request details: %s") % NexmoMessage(req).get_details()
    print NexmoMessage(req).send_request()

    print

    # my numbers
    req = {'api_secret': p, 'api_key': u, 'type': 'numbers'}
    print("request details: %s") % NexmoMessage(req).get_details()
    print NexmoMessage(req).send_request()

    print

    # pricing for country 'NL'
    req['type'] = 'pricing'
    req['country'] = 'NL'
    print("request details: %s") % NexmoMessage(req).get_details()
    print NexmoMessage(req).send_request()

    # text message
    msg['text'] = m
    sms1 = NexmoMessage(msg)
    print("SMS details: %s") % sms1.get_details()
    m += " ktnxbye"
    sms1.set_text_info(m)
    print("SMS details: %s") % sms1.get_details()
    print sms1.send_request()

if __name__ == "__main__":
    sys.exit(main())
