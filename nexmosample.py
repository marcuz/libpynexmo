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

    sms1 = NexmoMessage(s, u, p, f, t, m)
    print("SMS details: %s") % sms1.getDetails()
    print sms1.sendRequest()

    print

    sms2 = NexmoMessage(s, u, p, f, t)
    sms2.setBinInfo(bb, bu)
    print("SMS details: %s") % sms2.getDetails()
    print sms2.sendRequest()

if __name__ == "__main__":
    sys.exit(main());
