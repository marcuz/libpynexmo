#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from nexmomessage import NexmoMessage

def main():

    s = "http://rest.nexmo.com/sms/json"
    u = "changeme"
    p = "changeme"
    f = "marcuz"
    t = "+39**********"
    m = "fool the reader àèìòù !!!"
    bb = "0011223344556677"
    bu = "06050415811581"

    msg = {'server': s, 'password': p, 'from': f, 'to': t, 'username': u}

    msg['text'] = m
    sms1 = NexmoMessage(msg)
    print("SMS details: %s") % sms1.get_details()
    m += " ktnxbye"
    sms1.set_text_info(m)
    print("SMS details: %s") % sms1.get_details()
    print sms1.send_request()

    print

    sms2 = NexmoMessage(msg)
    sms2.set_bin_info(bb, bu)
    print("SMS details: %s") % sms2.get_details()
    print sms2.send_request()

    print

    msg['title'] = "this is a test"
    msg['url'] = "http://twitter.com/tmarcuz"
    msg['text'] = False
    sms3 = NexmoMessage(msg)
    print("SMS details: %s") % sms3.get_details()
    print sms3.send_request()

if __name__ == "__main__":
    sys.exit(main());
