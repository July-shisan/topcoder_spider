import os
modules = ['match', 'match_detail', 'problem', 'code']

for module in modules:
	os.system('scrapy crawl %s -t json -o incremental.json' % module)
	r = open('incremental.json', 'r').read()
	if len(r) > 2:
		s = open('%s.json' % module, 'r').read()[:-1]
		s += ',\n'
		s += r[1:]
		open('%s.json' % module, 'w').write(s)
	os.system('rm incremental.json')

