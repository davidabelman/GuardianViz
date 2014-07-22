"""
This file calcaultes TF-IDF values for articles, and saves them as extra key entries within article dictionary
Within options file we can specify the level of data we would like to use within TF-IDF
"""

import pickle
import options
reload(options)
from general_functions import *


def unzip_dict_contents(dictionary = None, combine_keys = ['tags']):
	"""
	Takes a dicitonary of things (each with an 'id' key in) and pulls out required fields in format:
	[(id, 'some stuff in form of string'), (id, 'some stuff in form of string'), (id, 'some stuff in form of string')]
	"""
	assert type(combine_keys)==list, "-- Assert error: keys to combine must be a list"
	output = []
	for id_ in dictionary:
		a = articles[id_]
		assert 'id' in a, "-- Assert error: all entries in dictionary must have a key called 'id'"
		total_string = ""
		for key in combine_keys:
			if type(a[key])==list:  # Join all elements in list separated by space (e.g. [list, of, tags] --> "list of tags")
				add_string = " ".join(a[key])
				total_string += add_string
			elif type(a[key])==unicode or type(a[key])==str:  # Just add the string as it is (e.g. body or headline)
				total_string += a[key]+" "
			else:
				print "-- Type %s not dealt with" %(type(a[key]))
		output.append( (a['id'], total_string ) )
	return output

def find_top_related_tfidf(query_tfidf, tfidf, ids, n=25):
	"""
	Returns zip lists of TF_IDFs and article IDs in form [(0.5, id), (0.44, id2) .... ]
	"""
	from sklearn.metrics.pairwise import linear_kernel
	cosine_similarities = linear_kernel(query_tfidf, tfidf).flatten()   # Multiple article TF-IDF with all others
	related_docs_indices = cosine_similarities.argsort()[:(-n-1):-1]  # Take top N results (excluding itself)
	ids_extracted = [ ids[x] for x in related_docs_indices ]
	# import pdb; pdb.set_trace()
	return zip(cosine_similarities[related_docs_indices], ids_extracted)  # [(0.5, id), (0.44, id2) .... ]

def add_tfidf( articles, combine_keys = ['tags','headline','standfirst'], output_title = 'tfidf', n=25, stopwords='english' ):
	"""
	The whole process:
	Adds TF-IDF elements to the articles data structure, according to the keys specified, and n
	"""
	from sklearn.feature_extraction.text import TfidfVectorizer
	# Decide which data to use to find TF-IDF, create dataset, perform TF-IDF
	article_tuples = unzip_dict_contents(articles, combine_keys)  # [(article_id, "blah blah blah"), (article_id, "blah blah blah"), (article_id, "blah blah blah")]
	ids, data = zip(*article_tuples)
	tfidf = TfidfVectorizer(stop_words=stopwords).fit_transform(data)

	# Find mutual similarities for all pairs of articles, write to articles file
	for i in range(len(ids)):
		query_tfidf = tfidf[i:i+1]
		articles[ids[i]][output_title] = find_top_related_tfidf(query_tfidf, tfidf, ids, n)
	return articles

def print_results(articles, key):
	"""
	Print 3 test cases out
	"""
	if options.tfidf_print_test_on:
		print "\nChecking random results (for key %s):\n" %(key)
		for rand in [25,12,1]:
			a = articles[articles.keys()[rand]]
			print "Original article:", a['id']
			print "--------------"
			print "Related:"
			for thing in a['tfidf_headline']:
				print thing
			print "\n\n"

# Load the articles
articles = load_pickle(options.current_articles_path)
stopwords = create_stopword_list(extra_words = options.tfidf_extra_stopwords)
length = options.tf_idf_list_length

if options.tfidf_tags:
	print "Calculating TFIDF for tags..."
	articles = add_tfidf ( articles, combine_keys = ['tags'], output_title = 'tfidf_tags', n=length, stopwords=stopwords )
if options.tfidf_headline:
	print "Calculating TFIDF for tags, headline..."
	articles = add_tfidf ( articles, combine_keys = ['tags','headline'], output_title = 'tfidf_headline', n=length, stopwords=stopwords )
if options.tfidf_standfirst:
	print "Calculating TFIDF for tags, headline, standfirst..."
	articles = add_tfidf ( articles, combine_keys = ['tags','headline','standfirst'], output_title = 'tfidf_standfirst', n=length, stopwords=stopwords )
if options.tfidf_body:
	print "Calculating TFIDF for tags, headline, standfirst, body..."
	articles = add_tfidf ( articles, combine_keys = ['tags','headline','standfirst', 'body'], output_title = 'tfidf_body', n=length, stopwords=stopwords )

# Print some example results just to sanity check
print_results(articles, 'tfidf_headline')

# Save pickle with TF-IDF data added
save_pickle( articles, options.current_articles_path )





