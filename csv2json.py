import sys
import json
import csv

from_file = sys.argv[1]
to_file = sys.argv[2]


reader = csv.reader(open(from_file, 'r'))

l = '['
keys = reader.next()

first = True
for items in reader:
	if first:
		ll = ''
		first = False
	else:
		ll = ',\n'
	ll += '{"' + keys[0] + '": "' + items[0] + '"'
	for i in xrange(1, len(items)):
		ll += ', "' + keys[i] + '": "' + items[i] + '"'
	ll += '}'
	l += ll
l += ']'

f = open(to_file, 'w')
f.write(l)
f.close()
