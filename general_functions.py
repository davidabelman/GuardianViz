"""
general_functions.py
General functions used within project
"""


def load_pickle(filename, silent = False):
	"""
	Loads pickle and prints to screen
	"""
	import pickle
	if not silent:
		print "Loading pickle (%s)" %(filename)
	try:
		return pickle.load( open( filename, "rb" ) )
	except:
		print "Error loading pickle."

def save_pickle(data, filename, silent = False):
	"""
	Saves pickle and prints to screen
	"""
	import pickle
	if not silent:
		print "Saving pickle (%s)" %(filename)
	pickle.dump( data, open( filename, "wb" ) )

def export_dict_to_json(data, path):
	"""
	Write a python element to JSON
	"""
	import json
	j = json.dumps(data)
	with open(path, 'w') as file_to_write:
		file_to_write.write(j)

def convert_str_to_date(string):
	"""
	Converts a string of format u'2013-06-24T23:06:02Z' into datetime.date (ignores time)
	"""
	from time import mktime, strptime
	from datetime import datetime
	struct = strptime(string[0:10], "%Y-%m-%d")
	dt = datetime.fromtimestamp(mktime(struct))
	return dt

def create_REST_request(main, parameters = []):
	"""
	Appends a list of parameters to a URL separating all with & sign.
	Output something like this:
	http://beta.content.guardianapis.com/world?api-key=explorer&page-size=76&order-by=oldest&use-date=published&show-tags=keyword&show-elements=all&show-story-package=true&show-related=true&show-most-viewed=true&show-fields=standfirst%2Cthumbnail%2Cbyline%2Cheadline%2Cbody
	"""
	for p in parameters:
		main += p+"&"
	print "Generated the following request: %s" %(main[:-1])
	return main[:-1]

def create_stopword_list(extra_words):
	"""
	Creates stopword list (adds extra words to original English set)
	"""
	from sklearn.feature_extraction.text import TfidfVectorizer
	original = list(TfidfVectorizer.get_stop_words(TfidfVectorizer(stop_words='english')))
	return frozenset(original+extra_words)