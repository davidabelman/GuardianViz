import pickle
import options
reload(options)
from general_functions import *

def unzip_dict_contents_modified(dictionary = None, combine_keys = ['tags']):
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

		# Extract first tag if it exists
		if len(a['tags'])==0:
			tag = 'Misc'
		else:
			tag = a['tags'][0]

		# Create list of tags and data
		output.append( (a['id'], tag, total_string ) )

	return output

def create_stopword_list(extra_words):
	"""
	Creates stopword list (adds extra words to original English set)
	"""
	from sklearn.feature_extraction.text import TfidfVectorizer
	original = list(TfidfVectorizer.get_stop_words(TfidfVectorizer(stop_words='english')))
	return frozenset(original+extra_words)

articles = load_pickle(options.current_articles_path)
stopwords = create_stopword_list(extra_words = options.tfidf_extra_stopwords)

from sklearn.feature_extraction.text import TfidfVectorizer
article_tuples = unzip_dict_contents_modified(articles, ['tags'])  # [(article_id, "blah blah blah"), (article_id, "blah blah blah"), (article_id, "blah blah blah")]
ids, tags, data = zip(*article_tuples)
tfidf = TfidfVectorizer(stop_words=stopwords).fit_transform(data)

from sklearn.decomposition import RandomizedPCA
pca = RandomizedPCA(n_components=2)
pca.fit(tfidf)
output=pca.fit_transform(tfidf)

# Plot the PCA output as it stands
import pylab as pl
o0 = range(len(output))  # Create indices
o1, o2 = zip(*output)[0], zip(*output)[1]
pl.scatter(o1,o2)
print "This is the PCA space for our articles (unmodified)"
pl.show()

# Fix at 15*16 block
to_fill = []   # we want [(0,4,2),(1,4,3),(2,9,1)] where we use (id, row, col)
import pandas
import numpy as np
df = pandas.DataFrame([o1,o2]).transpose()
df.columns = ['pca1','pca2']
df = df.sort(column='pca1')
df['pca1group']=o0
df['pca1group'] = df['pca1group'].apply(lambda x: np.floor(x*1.0/16))
df = df.sort(columns=['pca1group', 'pca2'])
df['pca2group']=o0
df['pca2group'] = df['pca2group'].apply(lambda x: x%16)
print df[0:35]

plot_list = []
for i in range(len(df)):
	index = df[i:i+1].index[0]
	tag = tags[index]
	pca1 = df['pca1group'][index]
	pca2 = df['pca2group'][index]
	plot_list.append((tag, pca1, pca2))


pl.scatter(zip(*plot_list)[1], zip(*plot_list)[2])
pl.rcParams.update({'font.size': 8})
for i in range(len(o0)):
	pl.annotate(zip(*plot_list)[0][i],xy=(zip(*plot_list)[1][i],zip(*plot_list)[2][i]))
pl.show()
