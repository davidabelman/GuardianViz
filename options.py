"""
Options
"""



path_choice = {
	'all' : "data/articles.p",

	'uk' : "data/articles_uk.p",
	
	'uk_1_wk' : "data/articles_uk_1_wk.p",

	'sample' : "data/articles_subset.p",
}
current_articles_path = path_choice [ 'uk_1_wk' ]

# Raw data from Guardian
raw_pickle_path = "data/world_data.p"
main_guardian_crawl_from_date = "2013-01-01"
main_guardian_crawl_to_date = "2013-02-28"
main_guardian_crawl_min_wait = 2
main_guardian_crawl_max_wait = 14

# Raw data from Facebook
facebook_stats_path = "data/fb.p"

# Raw data on Guardian links
guardian_links_path = "data/guardian_links.p"





overwrite_articles = True
find_internal_links = False  # This slows things down a lot, therefore can toggle off if not being used

articles_subset_size = 500

facebook_crawl_wait = 0.5

tfidf_print_test_on = True
tfidf_tags = True
tfidf_headline = True
tfidf_standfirst = True
tfidf_body = False
tfidf_extra_stopwords = ['video', 'eyewitness', 'pictures']
tf_idf_list_length = 100