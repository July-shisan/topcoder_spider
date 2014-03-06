def extract_text(xpath):
	l = xpath.extract()
	if len(l) > 0:
		return l[0].strip()
	else:
		return ''
