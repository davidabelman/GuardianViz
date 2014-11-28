"""
==============================
Butterfly effect visualisation
==============================

Notes:
1) Similarity value found between all pairs of articles based on tag, headline, and strapline. These are found by cosine similarity, and pairwise values are stored [TODO: either in a sparse matrix form, if we can store this within Flask, or in a database if we have to...]. We only need to store values if they are above a certain threshold. These are all calculated on a one off basis at first, and as new articles are crawled, we need to calculate pairwise similarity with all existing articles and store these values. Note that for each value stored, we need to store it either within 'future_articles' or 'past_articles'.

2) For all similar articles (say 20 of them) we run some type of clustering [TODO: topic analysis, LDA, or K-means] and form 2 or 3 topics of similar articles. Number of topics may depend on how many similar articles there are.

3) For each topic we want to select the most relevant article to display to the user. This should be based on its PageRank, its Facebook shares, and its date. Details to be decided...
"""

import time
import sys
import re
WORD = re.compile(r'\w+')
import math
import pprint
from collections import Counter
import options
import datetime
import general_functions
stopwords = general_functions.create_stopword_list(extra_words = options.tfidf_extra_stopwords)
debug = False


###### CREATING THE COSINE DICTIONARY #########
def get_cosine(vec1, vec2):
    """
    Gets cosine similarity between 2 dicts
    Form of input is: {'word1':4, 'word2':2...}
    """
    # Variables must be Counters of the form {'word1':4, 'word2':2...}
    
	# Calculate numerator (return 0 if no intersection)
    intersection = set(vec1.keys()) & set(vec2.keys())
    if len(intersection)<5:
    	return 0  # Avoid unecessary further calculation...
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    # Calculate denominator
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def count_terms(word_list):
	"""
	Creates a counter dictionary of terms, e.g. {'word1':4, 'word2':2...}
	Input is a list
	"""
	assert type(word_list)==list, "Input must be a list. We have %s" %(word_list)
	return Counter(word_list)

def string_to_list(string):
	"""
	Convert string to list
	'a string of words' --> ['a', 'string', 'of', 'words']
	"""
	return WORD.findall(string)

def remove_stopwords_and_convert_lower_case(l):
	"""
	Remove stopwords from a list
	"""
	return [x.lower() for x in l if x not in stopwords]

def compare_dates(date1, date2):
	"""
	Given 2 dates, compare if date2 is in the future or past
	Return 'future' or 'past'
	"""
	assert type(date1)==datetime.datetime and type(date2)==datetime.datetime
	if date2>date1:
		return 'future'
	else:
		return 'past'

def article_type_is_bad(id_str):
	"""
	Checks id_str (ID, e.g. 'world/gallery/2013/aug/19/pipe-band-championship-2013-glasgow') for banned terms, such as 'gallery', 'video', etc.
	Returns True if any banned terms found...
	"""
	check = id_str[0:30]  # Take only first part of ID
	banned_terms = ['video', 'gallery', 'interactive', 'commentisfree', 'blog', 'live', 'shortcuts']
	# Check each banned term
	for x in banned_terms:
		if x in check:
			return True
	# If no banned terms found
	else:
		return False

def create_vector_from_article(article, include_standfirst=False):
	"""
	Convert an article (which is a dictionary with keys of 'standfirst', 'tags', 'headline') into a count of terms within the values of these keys
	Output dictionary of counts
	Note that stopwords are removed and everything is converted to lowercase
	Example
	Input = {'headline':'John Major is grey', 'standfirst':'John Major really is', 'tags':'Major'}
	Output = {'John':2, 'Major':3, 'grey':1, 'really':1}
	"""
	headline = string_to_list(article['headline'])	
	tags = article['tags']
	if include_standfirst:
		standfirst = string_to_list(article['standfirst'])

	# Remove stopwords from headline and standfirst
	headline = remove_stopwords_and_convert_lower_case(headline)
	tags = remove_stopwords_and_convert_lower_case(tags)
	if include_standfirst:
		standfirst = remove_stopwords_and_convert_lower_case(standfirst)

	# Create list of all headline, standfirst and tags and count...
	return count_terms(headline+tags)
	if include_standfirst:
		return count_terms(headline+standfirst+tags)
	 

def create_cosine_similarity_pickle_all_articles(threshold=0.5, incremental_add=True):
	"""
	Create cosine similarity matrix for all articles currently existing
	Should only need to be run once (we can then add to it incrementally)
	Pickle will be saved to disk.
	Form of matrix is:
	{'article1': 
		{'past_articles':
			{'article5':0.71,
			 'article14': 0.88,
			 ...
			 }
		},
		{'future_articles':
			{'article9':0.99,
			 'article29': 0.73,
			 ...
			 }
		},
	}
	"""
	if incremental_add == False:
		# Everything will be recalculated from afresh
		# Check we want to overwrite the main pickle (will take a long time...)
		print "WARNING: Are you sure you wish recalculate all cosine similarity values??"
		print "This will overwrite all previous values and may take a long time."
		print "We will use *%s* as the article set." %options.current_articles_path
		print "If not, set incremental_add to True: this will only calculate new cosine pairs."
		print "Press 'y' to continue..."
		u = raw_input('>> ')
		if u!='y':
			print "** CANCELLED **"
			return None
		print "Creating cosine similarity matrix using %s" %options.current_articles_path

		# Empty variable to fill
		cosine_similarity_matrix = {}  # To fill with whole matrix

	elif incremental_add==True: 
		# We will only add the new articles and calculate pairs involving these
		cosine_similarity_matrix = general_functions.load_pickle(filename = options.current_articles_path_cosine_similarites)  # To add incremental articles to
		if cosine_similarity_matrix == None:
			print "-- WARNING: could not load similarity matrix. Does it exist already or do we need to switch off incremental mode (i.e. create new matrix)?\n"
			sys.exit()

	# Start timer
	t1 = time.time()

	# Load articles and start counter	
	articles = general_functions.load_pickle(options.current_articles_path)
	total_number = len(articles)
	counter = 0
	print "We have %s articles to loop through." %total_number

	# Loop through all articles in main collection	
	for id1 in articles:
		counter+=1
		print "Article %s/%s" %(counter, total_number)

		# Skip if article already in the cosine_similarity_matrix
		if id1 in cosine_similarity_matrix:
			print "Skipping article, already analysed"
			continue

		# Skip if article is not of type we like
		if article_type_is_bad(id1):
			print "Skipping article, bad type"
			continue

		# Load article
		article1 = articles[id1]
		article1_cosine_similarities = {'future_articles':{}, 'past_articles':{}}  # To fill with 1 row

		# Create vector (dict of counts) for the article
		article1_vector = create_vector_from_article(article1)
		if debug:			
			print "================================"
			print "article1:"
			print "Headline:", article1['headline']
			print "Tags:", article1['tags']		
			print "Vector created:", article1_vector

		# Loop through all second articles
		for id2 in articles:
			if id1==id2:
				continue
			if article_type_is_bad(id2):
				continue

			# Load article
			article2 = articles[id2]

			# Create vector (dict of counts) for the second article
			article2_vector = create_vector_from_article(article2)			
			if debug:
				print ""
				print "-- article2:"
				print "-- Headline:", article2['headline']
				print "-- Tags:", article2['tags']		
				print "-- Vector created:", article2_vector

			# Calculate crossover
			cosine = get_cosine(article1_vector, article2_vector)
			if debug:
				print "---- Cosine = %s" %cosine
			
			# Ignore second article if too low crossover
			if cosine<threshold:				
				if debug:
					print "---- Not storing, cosine too low"
				continue

			# Store in collection if crossover is over threshold
			# Stored as integer (/100) as saves 25% space
			date1, date2 = article1['date'], article2['date']
			future_or_past = compare_dates(date1, date2)
			cosine = int(cosine*100)

			if future_or_past=='future':
				article1_cosine_similarities['future_articles'][id2] = cosine
			elif future_or_past=='past':
				article1_cosine_similarities['past_articles'][id2] = cosine

			# Also add to corresponding 'other' article if it exists in the matrix already
			# Note that past/future are swapped, as we are comparing swapped dates to the above
			if id2 in cosine_similarity_matrix:
				if future_or_past=='future':
					cosine_similarity_matrix[id2]['past_articles'][id1] = cosine
				elif future_or_past=='past':
					cosine_similarity_matrix[id2]['future_articles'][id1] = cosine

		# Now we have looped through all articles, we add the line for id1 to our overall matrix
		cosine_similarity_matrix[id1] = article1_cosine_similarities
		if debug:
			print "======\n====="
			print "THIS IS THE SIMILARITY MATRIX LINE"
			pprint.pprint(cosine_similarity_matrix)

		# Save the pickle every 100 additions
		if counter%100==0:
			general_functions.save_pickle(data = cosine_similarity_matrix, filename = options.current_articles_path_cosine_similarites)

	# End for statement looping over id1. Save pickle.
	general_functions.save_pickle(data = cosine_similarity_matrix, filename = options.current_articles_path_cosine_similarites)
	
	# End timer
	t2 = time.time()
	print "TOTAL TIME:", t2 - t1


# Create a NEW cosine similarity dictionary and save as pickle for ALL articles
# WARNING: incremental_add=False means we start from a blank matrix
# create_cosine_similarity_pickle_all_articles(incremental_add=False)

# Update the cosine similarity dictionary and save as pickle for incremental articles
# incremental_add=True means we only add incremental articles
create_cosine_similarity_pickle_all_articles(incremental_add=True)


