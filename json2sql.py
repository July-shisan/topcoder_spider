import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from Problem import Problem

lineNO = int(open('generate_sql_line.txt').read())

lines = open('incremental_log.json', 'r').readlines()

import json

start_problem_line = json.loads(lines[lineNO])['problem']
end_problem_line = json.loads(lines[-1])['problem']

problems = json.loads(open('problem.json','r').read())


import io

f = io.open('problems.sql', 'a', encoding='utf-8')

for i in xrange(start_problem_line, end_problem_line):
	problem = Problem(problems[i])
	f.write(unicode(problem) + '\n')

f.close()	
