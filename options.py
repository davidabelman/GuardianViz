"""
Options
"""

raw_pickle_path = "data/world_data.p"
#raw_pickle_path = "data/test.p"
article_path = "data/articles.p"
article_subset_path = "data/articles_subset.p"
articles_uk_path = "data/articles_uk.p"
facebook_stats_path = "data/fb.p"
guardian_links_path = "data/guardian_links.p"

opencrawl_from_date = "2013-01-01"
opencrawl_to_date = "2013-02-28"

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