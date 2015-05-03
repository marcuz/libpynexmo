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
import copy

from nexmo import NexmoVerify


def main():

    r = "json"
    u = "changeme"
    p = "changeme"
    f = "marcuz"
    t = "44**********"

    msg = {'reqtype': r, 'api_secret': p, 'from': f, 'to': t, 'api_key': u}

    verify = copy.deepcopy(msg)

    try:
        if sys.argv[1] == 'verify':
            verify['number'] = sys.argv[2]
            verify['brand'] = sys.argv[3]
        elif sys.argv[1] == 'verify/check':
            verify['request_id'] = sys.argv[2]
            verify['code'] = sys.argv[3]
        elif sys.argv[1] == 'verify/search':
            verify['request_id'] = sys.argv[2]
        elif sys.argv[1] == 'verify/control':
            verify['request_id'] = sys.argv[2]
            verify['cmd'] = sys.argv[3]
        else:
            sys.exit('Request not supported: %s' % sys.argv[1])
    except IndexError:
        print('Missing parameters:')
        print('%s verify number brand' % sys.argv[0])
        print('%s verify/check request_id code' % sys.argv[0])
        print('%s verify/search request_id' % sys.argv[0])
        print('%s verify/control request_id cmd' % sys.argv[0])
        sys.exit()

    verify['type'] = sys.argv[1]
    r = NexmoVerify(verify)
    print("Details: %s") % (r.get_details())
    print r.send_request()

if __name__ == "__main__":
    sys.exit(main())
