import os
import io

class Problem:
	def convert(self, s):
		res = ''
		for c in s:
			if c == '\'':
				res += '\'\''
			else:
				res += c
		return res

	def solution(self, problem, lang):
		path = 'codes/' + problem['problem_id'] + '_' + lang
		if os.path.exists(path):
			return self.convert(io.open(path, 'r', encoding='utf-8').read())
		return ''

	def set_name(self, d):
		self.name = self.convert(d['name'])

	def set_content(self, d):
		path = d['content']
		if os.path.exists(path):
			self.content = self.convert(io.open(path, 'r', encoding='utf-8').read())
		self.content = ''
	
	def set_writer(self, d):
		self.writer = self.convert(d['writer'])

	def set_lv(self, d):
		lv1 = 0
		if len(d['level_div1']) != 0:
			lv1 = int(d['level_div1'])
		lv2 = 0
		if len(d['level_div2']) != 0:
			lv2 = int(d['level_div2'])
		self.lv = lv1 * 4 + lv2
		
	def set_date(self, d):
		self.date = self.convert(d['date'])
	
	def set_java(self, d):
		self.java = self.solution(d, 'Java')
	
	def set_csharp(self, d):
		self.csharp = self.solution(d, 'C#')

	def set_cpp(self, d):
		self.cpp = self.solution(d, 'C++')

	def set_vb(self, d):
		self.vb = self.solution(d, 'VB')

	def set_python(self, d):
		self.python = self.solution(d, 'Python')
	
	def set_problem_id(self, d):
		self.problem_id = d['problem_id']

	def __init__(self, d):
		self.set_name(d)
		self.set_content(d)
		self.set_writer(d)
		self.set_lv(d)
		self.set_date(d)	
		self.set_java(d)
		self.set_csharp(d)
		self.set_vb(d)
		self.set_cpp(d)
		self.set_python(d)
		self.set_problem_id(d)
	
	def __str__(self):
		sql_template = u'insert into problem(name, content, writer, level, date, solution_java, solution_csharp, solution_vb, solution_cpp, solution_python, problem_id) values(\'%s\', \'%s\', \'%s\', %d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s)';
		return sql_template % (self.name, self.content, self.writer, self.lv, self.date, self.java, self.csharp, self.vb, self.cpp, self.python, self.problem_id)
