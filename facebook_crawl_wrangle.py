"""
facebook_crawl_wrangle
Takes Facebook crawled data and adds it to the overall articles database
"""

import pickle
import options
reload(options)
from general_functions import *

articles = load_pickle(options.article_path)
fb = load_pickle(options.facebook_stats_path)

for f in fb:
	# Add Facebook data to articles data
	articles[f]['facebook'] = {'days':fb[f]['days'], 'snapshot_of_total':fb[f]['fb_total']}

for a in articles:
	if 'facebook' not in articles[a]:
		articles[a]['facebook'] = {'days':'Not extracted', 'snapshot_of_total':'Not extracted'}

save_pickle(articles, options.article_path)