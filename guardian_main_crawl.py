"""
Guardian open explore API.
This script pulls lists of articles between a certain range, including their body text, headline, tags, date...
Originally written to pull 'world' articles (easily changed below)
It cannot pull (sadly) related articles and story packages, as these only seem to appear when the request is that for a specific ID (e.g. world/2002/jan/10/colombia.martinhodgson, rather than 'world' by itself)
It saves these as a pickle.
In a later script these are then cleaned to a nicer format, removing redundant information.
Note that requests are not checked for duplicates, so be sure not to set date ranges already searched.
Best to leave reasonable gaps between API requests.
You can set the date range for the data pulled. 
See options.py.
"""

import urllib2
import json
import pickle
import time
import random
import options
reload(options)
import general_functions
reload(general_functions)
from general_functions import *

# These are some of the parameters we can use...
# http://beta.content.guardianapis.com/AbelQuery?api-key=explorer (this displays a section of the paper(?), i.e. 'world')
# http://beta.content.guardianapis.com/search?q=AbelQuery&api-key=explorer (this searches for a specific article by TF-IDF?)
# http://beta.content.guardianapis.com/sections?q=AbelQuery&api-key=explorer
# http://beta.content.guardianapis.com/tags?q=AbelQuery&api-key=explorer
# &from-date=2014-07-02
# &to-date=2014-07-03
# &page=75
# &page-size=76
# &order-by=newest
# &use-date=published
# &show-tags=keyword
# &show-elements=all
# &show-story-package=true
# &show-related=true
# &show-most-viewed=true
# &show-fields=standfirst%2Cthumbnail%2Cbyline%2Cheadline%2Cbody
# &api-key=explorer
# &api-key=uu4qhyqqknrkhrsmahfwr2qs


def how_many_pages():
	"""
	Discovers how many pages in the request to be carried out
	"""
	request = create_REST_request(main, parameters)
	response = urllib2.urlopen(request).read()
	data = json.loads(response)
	return data['response']['pages']

# Options
data_pickle_path = options.raw_pickle_path

# Set up the parameters
main = "http://beta.content.guardianapis.com/world?"
api_key = "api-key=uu4qhyqqknrkhrsmahfwr2qs"
from_date = "from-date="+convert_datetime_to_str(options.crawl_start_datetime)
to_date = "to-date="+convert_datetime_to_str(options.crawl_end_datetime)
use_date = "use-date=published"
order_by = "order-by=newest"
page_size = "page-size=76"
show_tags = "show-tags=keyword"
show_elements = "show-elements=all"
show_story_package = "show-story-package=true"
show_most_viewed = "show-most-viewed=true"
show_fields = "show-fields=standfirst,thumbnail,byline,headline,body"
page = "page=1"

parameters = [	api_key,
				from_date,
				to_date,
				use_date,
				order_by,
				page_size,
				show_tags,
				show_elements,
				show_story_package,
				show_fields,
				page
				]

# Assess how many pages there are with a single first request
total_pages = how_many_pages()

# Open up the pickles
data_store = load_pickle(data_pickle_path)

counter = 0

for i in range(total_pages):

	# Sleep for random time
	min_wait = options.main_guardian_crawl_min_wait
	max_wait = options.main_guardian_crawl_max_wait
	time.sleep( random.randint(min_wait*10,max_wait*10)*1.0/10 )
	page_number = i+1
	print "Now pulling page number %s/%s" %(page_number, total_pages)

	# Update page part of parameters, create request
	parameters.pop() # Get rid of old page number
	parameters.append("page=%s" %(page_number)) # Add new page number
	request = create_REST_request(main, parameters)

	# Now pull the data
	response = urllib2.urlopen(request).read()
	page_data = json.loads(response); 	print "Pulled data and loaded into JSON format"

	# Add data to pickle
	data_store.append(page_data)
	counter += 1
	if counter%30==0:
		save_pickle ( data_store, data_pickle_path )

save_pickle ( data_store, data_pickle_path )
	




