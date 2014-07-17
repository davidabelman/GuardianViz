"""
Takes articles set, creates smaller subsets (i.e. world/uk 2, 7, 30 days, etc.) to work with
Then using PCA and K-means to calculate some features, writes output of articles in a grid format (x, y coords) in JSON,
This is then used with a d3 script to plot articles in HTML
"""

import pickle
import options
reload(options)
from general_functions import *
import datetime

plot_pca = False
plot_grid = False
silent = True

def unzip_dict_contents_modified(dictionary = None, combine_keys = ['tags']):
	"""
	Takes a dicitonary of things (each with an 'id' key in) and pulls out required fields in format:
	[(id, 'some stuff in form of string'), (id, 'some stuff in form of string'), (id, 'some stuff in form of string')]
	"""
	assert type(combine_keys)==list, "-- Assert error: keys to combine must be a list"
	output = []
	for id_ in dictionary:
		a = dictionary[id_]
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
		'tags' : [''],
		'fb' : a['facebook']['snapshot_of_total'] if a['facebook']['snapshot_of_total']!='Not extracted' else 5,
		'url' : '#',
		'img' : '#',
		'headline' : 'No article here',
		'standfirst' : 'Hover over other articles or try changing the visualisation options.',
		'cluster' : '1',
		'date' : '',
		'saturation' : 0,
		'recency' : 38
		#'r' : str(cluster+1), #k_centres_2d[cluster][0]+np.random.randint(-10,10)*1.0/90,
		#'g' : 100, #np.random.randint(140,150),
		#'b' : str(cluster) #k_centres_2d[cluster][1]+np.random.randint(-10,10)*1.0/90,
		})
	return plot_list

def calculate_grid(articles):
	"""
	Calculate grid parameters to be sent to HTML, using input article set
	"""
	# Stop words
	stopwords = create_stopword_list(extra_words = options.tfidf_extra_stopwords)

	# Implement TF-IDF to get an output matrix based on tags, headline, standfirst etc.
	from sklearn.feature_extraction.text import TfidfVectorizer
	article_tuples = unzip_dict_contents_modified(articles, options.grid_features_to_use)  # [(article_id, "blah blah blah"), (article_id, "blah blah blah"), (article_id, "blah blah blah")]	
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
	import numpy as np
	number_of_clusters = int(np.ceil(len(output)**0.33)+1)
	k_means = KMeans(init='k-means++', n_clusters=number_of_clusters, n_init=10)
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

	if not silent:
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
			'fb' : np.ceil(np.sqrt(a['facebook']['snapshot_of_total'])) if a['facebook']['snapshot_of_total']!='Not extracted' else 5,
			'url' : a['url'],
			'img' : a['thumbnail'],
			'headline' : a['headline'],
			'standfirst' : a['standfirst'],
			'cluster' : str(cluster_map[cluster]),
			'date' : str(a['date'])[0:10],
			'saturation' : 0.6,
			'recency' : int((datetime.datetime.now()-a['date']).days)
			})

	# Add any remaining squares in grey to make sure we have a rectangle
	# plot_list = fill_out_rectangle(plot_list)

	# Return all data
	return plot_list

	
# Load articles
articles_main = load_pickle("data/articles.p")

# Go through combinations of articles to extract
tags = {'uk':'UK news', 'world':'World news'}
for day_range in [2,7,30]:
	now = datetime.datetime.now() #datetime.datetime(2014,6,30)
	end_date = now
	start_date = now-datetime.timedelta(days=day_range)
	for tag in tags:
		# Calculate articles
		article_set = {}
		for a in articles_main:
			if tags[tag] in articles_main[a]['tags'] and articles_main[a]['date'] >= start_date and articles_main[a]['date'] <= end_date:
				article_set[a] = articles_main[a]
		# Create grid
		grid = calculate_grid(article_set)
		# Write to a JSON file
		path = 'html/json/%s_%s.json' %(tag, day_range)
		export_dict_to_json(grid, path)

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
