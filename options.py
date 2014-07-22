"""
Options
"""
import datetime
from general_functions import *

# Paths
path_choice = {
	'all' : "data/articles.p",
	'uk' : "data/articles_uk.p",
	'uk_1_wk' : "data/articles_uk_1_wk.p",
	'sample' : "data/articles_subset.p",
}
current_articles_path = path_choice [ 'all' ]
crawl_start_datetime = datetime.datetime(2014,7,18)
crawl_end_datetime = datetime.datetime(2014,7,21)

# Raw data from Guardian
raw_pickle_path = "data/world_data.p"
main_guardian_crawl_min_wait = 5
main_guardian_crawl_max_wait = 8

# Main guardian crawl wrangle
overwrite_articles = True
find_internal_links = False  # This slows things down a lot, therefore can toggle off if not being used

# Raw data from Facebook
facebook_stats_path = "data/fb.p"
facebook_crawl_wait = 0.5
facebook_crawl_tag_filter = 'UK news'  # e.g. 'UK news'

# Raw data on Guardian links
guardian_links_path = "data/guardian_links.p"
guardian_links_crawl_tag_filter = 'UK news'  # e.g. 'UK news'
guardian_link_crawl_min_wait = 1
guardian_link_crawl_max_wait = 5

# Creating subsets
articles_subset_size = 500

# Creating TF-IDF links
tfidf_print_test_on = True
tfidf_tags = True
tfidf_headline = True
tfidf_standfirst = True
tfidf_body = True
tfidf_extra_stopwords = ['video', 'eyewitness', 'pictures']
tf_idf_list_length = 20

# Creating HTML grid
grid_features_to_use = ['tags', 'headline']