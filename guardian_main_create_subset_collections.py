"""
This script creates subsets of the main 'articles' pickle (which should contain everything we ever crawl from the Guardian website)
"""

import pickle
import options
reload(options)
from general_functions import *

# Load the articles (always want full collection in this case, when creating subsets)
articles = load_pickle(options.path_choice['all'])

# Small subset of X articles
print "Creating a small subset with %s articles" %(options.articles_subset_size)
count = 0
small = {}
for a in articles:
	if count>options.articles_subset_size:
		save_pickle (small, options.path_choice['sample'])
		break
	small[a] = articles[a]
	count += 1

# Subset of UK news only
print "Creating a UK subset"
uk = {}
for a in articles:
	if 'UK news' in articles[a]['tags']:
		uk[a] = articles[a]
save_pickle (uk, options.path_choice['uk'])

# Subset of 1 week of UK articles
import datetime
print "Creating 1 week of UK articles"
uk_1_wk = {}
for a in articles:
	if articles[a]['date'] > datetime.datetime(2014, 6, 9, 0, 0) and articles[a]['date'] < datetime.datetime(2014, 6, 17, 0, 0):
		uk_1_wk[a] = articles[a]
save_pickle (uk_1_wk, options.path_choice['uk_1_wk'])