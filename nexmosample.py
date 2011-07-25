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

    sms1 = NexmoMessage(s, u, p)
    sms1.textMessage(f, t, m)
    sms1.sendRequest()

    sms2 = NexmoMessage(s, u, p, f, t, m)
    sms2.sendRequest()

if __name__ == "__main__":
    sys.exit(main());
