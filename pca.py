import pickle
import options
reload(options)
from general_functions import *

plot_pca = False
plot_grid = False

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
			if type(a[key])==list:  # Join all elements in list separated by space, replacing any spaces (e.g. ['my list', 'of', 'tags'] --> "mylist of tags")
				add_string = " ".join([s.replace(" ","") for s in a[key]])
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

def rank_cluster_posns(positions):
	"""
	Take 2d array of positions, and return dictionary of cluster mappings so that the new '1' will be the left-most cluster etc.
	"""
	return_dict = {}
	x_dim = zip(*positions)[0]
	y_dim = zip(*positions)[1]
	combined = []
	for i in range(len(x_dim)):
		combined.append(x_dim[i]+y_dim[i])
	t = zip(combined, range(len(x_dim)))
	mapped = sorted(t, key=lambda x: x[0])
	clusters = range(len(x_dim))
	for i in range(len(mapped)):
		return_dict[clusters[i]]=mapped[i][1]
	return return_dict


def fill_out_rectangle(plot_list):
	"""
	Adds extra elements to plot list to ensure we have an equal sized grid
	Finds largest pca1group value, counts it, and counts second largest pca1group value
	Then adds grey squares for these
	"""
	maximal = max([entry['x'] for entry in plot_list])
	number_to_increase = len([entry['x'] for entry in plot_list if entry['x']==maximal])
	full_number = len([entry['x'] for entry in plot_list if entry['x']==maximal-1])
	for x in range(full_number-number_to_increase):
		plot_list.append({
		'index' : '',
		'id' : '',
		'x' : full_number,
		'y' : full_number-x-1,
		'tags' : ['None'],
		'fb' : a['facebook']['snapshot_of_total'] if a['facebook']['snapshot_of_total']!='Not extracted' else 5,
		'url' : '#',
		'img' : '#',
		'headline' : '',
		'standfirst' : '',
		'cluster' : '1',
		#'r' : str(cluster+1), #k_centres_2d[cluster][0]+np.random.randint(-10,10)*1.0/90,
		#'g' : 100, #np.random.randint(140,150),
		#'b' : str(cluster) #k_centres_2d[cluster][1]+np.random.randint(-10,10)*1.0/90,
		})
	return plot_list

# Load articles and stopwords
articles = load_pickle(options.current_articles_path)
stopwords = create_stopword_list(extra_words = options.tfidf_extra_stopwords)

# Implement TF-IDF to get an output matrix based on tags, headline, standfirst etc.
from sklearn.feature_extraction.text import TfidfVectorizer
article_tuples = unzip_dict_contents_modified(articles, ['tags', 'headline'])  # [(article_id, "blah blah blah"), (article_id, "blah blah blah"), (article_id, "blah blah blah")]
ids, tags, data = zip(*article_tuples)
tfidf = TfidfVectorizer(stop_words=stopwords).fit_transform(data)

# Apply PCA on the TF-IDF output
from sklearn.decomposition import RandomizedPCA
pca = RandomizedPCA(n_components=2)
pca.fit(tfidf)
output=pca.fit_transform(tfidf)
o0 = range(len(output))  # Create indices of articles
o1, o2 = zip(*output)[0], zip(*output)[1]  # Separate out the PCA components into lists

# Apply k-means clustering on the TFIDF output
from sklearn.cluster import KMeans
k_means = KMeans(init='k-means++', n_clusters=6, n_init=10)
k_means.fit(tfidf)
k_means_labels = k_means.labels_
k_centres_2d = pca.fit_transform(k_means.cluster_centers_)
cluster_map = rank_cluster_posns(k_centres_2d)

# Optional : Plot the PCA output as it stands
import pylab as pl
if plot_pca:
	print "This is the PCA space for our articles (unmodified)"
	pl.scatter(o1,o2)
	pl.show()

# Create an N*N block where N is ceil(sqrt) of total number of articles
import pandas
import numpy as np
N = np.floor(np.sqrt(len(output)))
df = pandas.DataFrame([o1,o2]).transpose()
df.columns = ['pca1','pca2']

# Label PCA1 with label between 0 and N
df = df.sort(column='pca1')
df['pca1group']=o0
df['pca1group'] = df['pca1group'].apply(lambda x: np.floor(x*1.0/N))

# Label PCA2 with label between 0 and N (sorted within each PCA1 label)
df = df.sort(columns=['pca1group', 'pca2'])
df['pca2group']=o0
df['pca2group'] = df['pca2group'].apply(lambda x: x%N)

print "Here is the PCA dataframe with the grouped (%s x %s) data:" %(N, N)
print df[0:35]
print "etc..."
print df

# Extract data from dataframe to JSON for visualisation
plot_list = []
for i in range(len(df)):
	index = df[i:i+1].index[0]
	id_ = ids[index]
	cluster = k_means_labels[index]
	pca1 = df['pca1group'][index]
	pca2 = df['pca2group'][index]
	a = articles[id_]
	plot_list.append({
		'index' : str(index),
		'id' : id_,
		'x' : pca1,
		'y' : pca2,
		'tags' : a['tags'],
		'fb' : a['facebook']['snapshot_of_total'] if a['facebook']['snapshot_of_total']!='Not extracted' else 5,
		'url' : a['url'],
		'img' : a['thumbnail'],
		'headline' : a['headline'],
		'standfirst' : a['standfirst'],
		'cluster' : str(cluster_map[cluster]),
		})

# Add any remaining squares in grey to make sure we have a rectangle
plot_list = fill_out_rectangle(plot_list)

import json
j = json.dumps(plot_list)
with open('html/grid.json', 'w') as the_file:
	the_file.write(j)

# Plot internally within Python
if plot_grid:
	plot_list = []
	for i in range(len(df)):
		index = df[i:i+1].index[0]
		tag = tags[index]
		cluster = k_means_labels[index]
		pca1 = df['pca1group'][index]
		pca2 = df['pca2group'][index]
		plot_list.append((tag, pca1, pca2, cluster))


	pl.scatter(zip(*plot_list)[1], zip(*plot_list)[2])
	pl.rcParams.update({'font.size': 8})
	for i in range(len(o0)):
		r = 7
		rand_a, rand_b = np.random.randint(-r,r)*1.0/20, np.random.randint(-r,r)*1.0/20
		pl.annotate(str(zip(*plot_list)[3][i])+" "+zip(*plot_list)[0][i],xy=((zip(*plot_list)[1][i])+rand_a,(zip(*plot_list)[2][i])+rand_b))
	pl.show()


# Export all required data to JSON (facebook , cluster, URL , image, pagerank, etc.)