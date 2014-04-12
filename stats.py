f = open('codes.csv', 'r')
lines = f.readlines()
f.close()

count = 0

failed = set()
all_code = set()
for line in lines[1:]:
	items = line.split(',')
	pid = items[-1].strip()
	status = items[0]
	if status == 'Failed!':
		failed.add(pid)
		count += 1
	all_code.add(pid)

f = open('problems.csv', 'r')
lines = f.readlines()
f.close()

not_crawled = set()

for line in lines[1:]:
	items = line.split(',')
	pid = items[-2]
	if pid not in all_code:
		not_crawled.add(pid)

print len(failed)
print len(not_crawled)		
print count	


s = set()

f = open('codes.csv', 'r')
code_lines = f.readlines()
lines = [code_lines[0]]
for line in code_lines[1:]:
	if line.split(',')[0] == 'Success':
		lines.append(line)
		s.add(line)
f.close()

f = open('sup_codes.csv', 'r')
sup_code_lines = f.readlines()
for line in sup_code_lines[1:]:
	if line.split(',')[0] == 'Success' and line not in s:
		lines.append(line)
		s.add(line)
f.close()

f = open('c_codes.csv', 'w')
f.write(''.join(lines))
f.close()

for line in lines[1:]:
	items = line.split(',')
	pid = items[-1].strip()
	lang = items[-2]
	name = pid + '_' + lang
	import os
	if not os.path.exists('codes/'+name):
		print line
s = set(lines)
print len(s)
print len(lines)

f = open('codes.csv', 'r')
lines = f.readlines()
f.close()

failed = set()
for line in lines:
	if line.split(',')[0] == 'Failed!':
		failed.add(line.split(',')[1])

for line in lines:
	if line.split(',')[0] == 'Success' and line.split(',')[1] in failed:
		print line
	
