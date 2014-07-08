"""
guardian_link_crawl
Goes through articles and requests article by article from the Guardian to collect data on the related articles and story packages
Pulls any related stories etc looking both into the future and into the past.
We will later filter out ones looking into the future, and only build our graph looking backwards (i.e. rebuild the future looking ones via backward looking ones)
"""

import urllib2
import json
import pickle
import options
reload(options)
import general_functions
reload(general_functions)
import time
import random
from general_functions import *


articles = load_pickle(options.article_path)
guardian_links = load_pickle(options.guardian_links_path)

# Will look something like this:
# http://beta.content.guardianapis.com/sport/2014/jul/06/novak-djokovic-v-roger-federer-wimbledon-2014-final-live,sport/2014/jul/06/andy-murray-virginia-wade-wimbledon-2014?api-key=explorer&page-size=76&order-by=newest&use-date=published&show-story-package=true&show-related=true&show-most-viewed=true

# Set up the parameters
main = "http://beta.content.guardianapis.com/"
api_key = "api-key=explorer"
show_story_package = "show-story-package=true"
show_related = "show-related=true"
show_most_viewed = "show-most-viewed=true"

parameters = [	api_key,
				show_story_package,
				show_related,
				show_most_viewed,
				]

counter = 0

#Loop through all articles
for a in articles:

	# Don't redo any we have already done
	if a not in guardian_links:
		
		# Filter by a certain tag for now
		if 'UK news' in articles[a]['tags']:

			# We will create a request
			main_with_id = main + a + '?'
			request = create_REST_request(main_with_id, parameters)
			
			# Now pull the data
			response = urllib2.urlopen(request).read()
			article_data = json.loads(response); 	print "Pulled data and loaded into JSON format"
			if article_data['response']['status'] != 'ok':
				print "Status not OK!"
				save_pickle ( guardian_links, options.guardian_links_path )
				exit()

			# Add data to pickle
			guardian_links.append(article_data)
			counter+=1
			if counter%5==0:
				save_pickle ( guardian_links, options.guardian_links_path )

			# Sleep for X seconds
			min_wait = 1
			max_wait = 6
			time.sleep( random.randint(min_wait*10,max_wait*10)*1.0/10 )

# Final save pickle
save_pickle ( guardian_links, options.guardian_links_path )
