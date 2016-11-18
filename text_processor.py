import re

def remove_links(tokens):
	to_remove = []
	for i in range(len(tokens)):
		if "http" in tokens[i] or "https" in tokens[i]:
			to_remove.append(i)
	for i in sorted(to_remove, reverse=True):
		del tokens[i]
	return tokens

def remove_retweet(tokens):
	if len(tokens) > 2 and tokens[0] == "rt":
		del tokens[1]
		del tokens[0]
	return tokens

def replace_unicode(text):
	text = text.replace('\\u2018', '\'')
	text = text.replace('\\u2019', '\'')
	text = text.replace('\\u2026', '...')
	text = text.replace('\\u00a0', ' ')
	text = text.replace('\\\"', '')
	text = re.sub("\\\\u....", '', text)
	return text

# stop_words should be a set
def process_text(text, stop_words):
	text = replace_unicode(text)
	tokens = re.split(' |\n|,|\\\\n|=', text)
	tokens = remove_links(tokens)
	tokens = [t.lower() for t in tokens]
	tokens = remove_retweet(tokens)
	tokens = [t.strip(',.?\'":;[]{}-_()!~|') for t in tokens]
	tokens = [t for t in tokens if not t in stop_words]
	tokens = [t for t in tokens if t != '']
	return ' '.join(tokens)
