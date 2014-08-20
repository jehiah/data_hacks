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
from decimal import Decimal
from optparse import OptionParser
from collections import defaultdict

def run(stream, options):
    count = 0
    skipped = 0
    data = defaultdict(int)
    if options.max:
        max_v = Decimal(options.max)
    for line in stream:
        line = line.strip()
        if not line:
            # skip empty lines (ie: newlines)
            continue
        try:
            if options.agg_values:
                key, value = line.split()
                value = int(value)
            else:
                key = line
                value = 1
            t = Decimal(key)
        except:
            print >>sys.stderr, "invalid line %r" % line
            continue
        if options.max and t > max_v:
            skipped += value
            continue
        count += value              
        data[t] += value
    calc_percentiles(data, count)
    if skipped:
        print skipped, "values outside of min/max"
        
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
    parser = OptionParser()
    parser.usage = "cat data | %prog [options]"
    parser.add_option("-a", "--agg-values", dest="agg_values", default=False, action="store_true",
                        help="Two column input format, space seperated with key<space>value")
    parser.add_option("-x", "--max", dest="max", help="maximum value")
    
    (options, args) = parser.parse_args()


    if sys.stdin.isatty():
        parser.print_usage()
        print "for more help use --help"
        sys.exit(1)
    run(sys.stdin, options)
