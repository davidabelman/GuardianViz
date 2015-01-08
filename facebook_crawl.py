"""
Gets Facebook 'like' stats for articles, and saves these to a separate pickle.
"""
import pickle
import options
reload(options)
from general_functions import *
import datetime
import urllib2


# https://graph.facebook.com/fql?q=select%20%20total_count%20from%20link_stat%20where%20url=%22http://www.theguardian.com/sport/2014/jul/06/novak-djokovic-wins-wimbledon-title-roger-federer%22

def get_facebook_likes(article_id):
	"""
	Returns the current number of FB likes for an article (sleeps after request, set time in options)
	"""
	import json
	import time
	import sys

	# Generate FQL request
	url = 'http://www.theguardian.com/'+article_id
	request = 'https://graph.facebook.com/fql?q=select%20total_count%20from%20link_stat%20where%20url=%22'+url+'%22'
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


# Load articles and already collected facebook links
articles = load_pickle(options.current_articles_path)
fb = load_pickle(options.facebook_stats_path)
silent = True

# Set start and end dates
start_date = options.crawl_start_datetime
end_date = options.crawl_end_datetime
tag_filter = options.facebook_crawl_tag_filter

# Assess how many requests we will be making in this session
total_counter = 0
for a in articles:
	if a not in fb:
		if tag_filter in articles[a]['tags'] and articles[a]['date']>=start_date and articles[a]['date']<=end_date:
			total_counter+=1
print "We will be requesting %s URLs in this session." %(total_counter)

# For each article:
count = 0
for a in articles:

	# Don't re-pull anything twice (for now)
	if a in fb:
		if not silent:
			print "We have already crawled this ID from Facebook: %s" %(a)
		continue

	else: 
		# Collect Facebook shares and age of article
		article_age = abs((articles[a]['date']-datetime.datetime.now()).days)
		
		if tag_filter in articles[a]['tags'] and articles[a]['date']>=start_date and articles[a]['date']<=end_date:
			likes = get_facebook_likes(a)
			if likes == "Unknown (failed request)":
				# Exit if failed to pull FB data
				save_pickle(fb, options.facebook_stats_path)
				import sys
				sys.exit("EXITING DUE TO FACEBOOK CRAWL ERROR.")
			# Providing we pulled data OK...
			fb[a] = {'days':article_age, 'fb_total':likes}
			count+=1
			print "We have pulled %s/%s pages.\n" %(count,total_counter)
			
			# Save pickle every 30 requests
			if count%30 == 0:
				save_pickle(fb, options.facebook_stats_path)
			


# Save pickle before exit
save_pickle(fb, options.facebook_stats_path)

if False:
	# Optional: Normalise all FB share data for old articles (older articles will have more shares as not collected at 3 day point)
	fb_share_rate_data = {}
	for a in fb:
		days = fb[a]['days']
		total = fb[a]['fb_total']
		if days not in fb_share_rate_data:
			fb_share_rate_data[days] = [ 1, total, 'to_be_replaced' ]
		else:
			fb_share_rate_data[days][0] += 1
			fb_share_rate_data[days][1] += total

	# Loop through days and work out average
	for d in fb_share_rate_data:
		fb_share_rate_data[d][2] = fb_share_rate_data[d][1]*1.0/fb_share_rate_data[d][0]

	for i in range(10):
		if i in fb_share_rate_data:
			print "On Day %s we have an average of %s shares..." %(i, fb_share_rate_data[i][2])
	print "(Need to make the call whether we should normalise share data out. Currently not.)"