#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from nexmomessage import NexmoMessage

def main():

    r = "json"
    u = "changeme"
    p = "changeme"
    f = "marcuz"
    t = "+39**********"
    m = "fool the reader àèìòù !!!"
    bb = "0011223344556677"
    bu = "06050415811581"

    msg = {'reqtype': r, 'password': p, 'from': f, 'to': t, 'username': u}

    # account balance
    req = {'password': p, 'username': u, 'type': 'balance'}
    print("request details: %s") % NexmoMessage(req).get_details()
    print NexmoMessage(req).send_request()

    print

    # pricing for country 'NL'
    req['type'] = 'pricing'
    req['country'] = 'NL'
    print("request details: %s") % NexmoMessage(req).get_details()
    print NexmoMessage(req).send_request()

    print

    # text message
    msg['text'] = m
    sms1 = NexmoMessage(msg)
    print("SMS details: %s") % sms1.get_details()
    m += " ktnxbye"
    sms1.set_text_info(m)
    print("SMS details: %s") % sms1.get_details()
    print sms1.send_request()

    print

    # bin message
    sms2 = NexmoMessage(msg)
    sms2.set_bin_info(bb, bu)
    print("SMS details: %s") % sms2.get_details()
    print sms2.send_request()

    print

    # wap message
    msg['title'] = "this is a test"
    msg['url'] = "http://twitter.com/tmarcuz"
    msg['text'] = False
    sms3 = NexmoMessage(msg)
    print("SMS details: %s") % sms3.get_details()
    print sms3.send_request()

if __name__ == "__main__":
    sys.exit(main());
