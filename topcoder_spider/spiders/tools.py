def extract_text(xpath):
	l = xpath.extract()
	if len(l) > 0:
		return l[0].strip()
	else:
		return ''

def get_param(url, param):
	import urlparse
	par = urlparse.parse_qs(urlparse.urlparse(url).query)
	if not par.has_key(param):
		return None
	return par[param][0]
