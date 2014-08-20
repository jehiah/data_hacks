#!/usr/bin/env python
# 
# Copyright 2010 bit.ly
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Calculate the percentiles from a list of values given on stdin

http://github.com/bitly/data_hacks
"""

import sys
import os
from decimal import Decimal

def run():
    count = 0
    data = {}
    for line in sys.stdin:
        line = line.strip()
        if not line:
            # skip empty lines (ie: newlines)
            continue
        key, value = line.split()
        try:
            t = Decimal(key)
        except:
            print >>sys.stderr, "invalid line %r" % line
        count += int(value)
        data[t] = data.get(t, 0) + int(value)
    calc_percentiles(data, count)
        
def calc_percentiles(data, count):
    # find the time it took for x entry, where x is the threshold
    percentile = 0
    
    threshold = Decimal(count) * Decimal('.01') * Decimal(percentile)
    start = Decimal(0)
    values = data.keys()
    values.sort()
    for t in values:
        # increment our count by the # of items in this time bucket
        start += data[t]
        while start > threshold and percentile <= 100:
            print "%02d%%" % percentile, t
            percentile += 1
            threshold = Decimal(count) * Decimal('.01') * Decimal(percentile)
    print "%02d%%" % percentile, values[-1]
    print "records", count
    

if __name__ == "__main__":
    if sys.stdin.isatty() or '--help' in sys.argv or '-h' in sys.argv:
        print "Usage: cat data | %s" % os.path.basename(sys.argv[0])
        sys.exit(1)
    run()
