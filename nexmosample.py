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
