"""
Gets Facebook like stats for articles and save to a separate pickle
"""
import pickle
import options
reload(options)
from general_functions import *

# https://graph.facebook.com/fql?q=select%20%20total_count%20from%20link_stat%20where%20url=%22http://www.theguardian.com/sport/2014/jul/06/novak-djokovic-wins-wimbledon-title-roger-federer%22

def get_facebook_likes(article_id):
	"""
	Returns the current number of FB likes for an article (sleeps after request, set time in options)
	"""
	import urllib2
	import json
	import time

	# Generate FQL request
	url = 'http://www.theguardian.com/'+article_id
	request = 'https://graph.facebook.com/fql?q=select%20total_count%20from%20link_stat%20where%20url=%22'+url+'%22'
	print request
	print "Generated the following request: %s" %(request)

	# Get the response
	try:
		response = urllib2.urlopen(request).read()
		print response
		json = json.loads(response)
		print "Converted to JSON. Sleeping for %s second(s)." %(options.facebook_crawl_wait)
		time.sleep(options.facebook_crawl_wait)
		return json['data'][0]['total_count']
	except:
		print "Failed to pull Facebook data"
		time.sleep(options.facebook_crawl_wait)
		return "Unknown (failed request)"


articles = load_pickle(options.article_path)
fb = load_pickle(options.facebook_stats_path)

# For each article:
count = 0
for a in articles:

	# Don't re-pull anything twice (for now)
	if a in fb:
		print "We have already crawled this ID from Facebook: %s" %(a)
		continue

	else: 
		# Collect Facebook shares and age of article
		article_age = abs((articles[a]['date']-datetime.now()).days)
		
		if 'UK news' in articles[a]['tags']:
			likes = get_facebook_likes(a)
			fb[a] = {'days':article_age, 'fb_total':likes}
			count+=1
			
			# Save pickle every 10 requests
			if count%10 == 0:
				save_pickle(fb, options.facebook_stats_path)
			


# Save pickle before exit
save_pickle(fb, options.facebook_stats_path)

# Optional: Normalise all FB share data for old articles (older articles will have more shares as not collected at 3 day point)
