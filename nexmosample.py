#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2013 Marco Londero <marco.londero@linux.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
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
