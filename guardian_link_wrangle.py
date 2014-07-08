"""
guardian_link_wrangle.py
Adds the guardian links crawled previously to the main article data
Adds both related content and story packages
"""

import pickle
import options
reload(options)
from general_functions import *

articles = load_pickle(options.current_articles_path)
guardian_links = load_pickle(options.guardian_links_path)

# Loop through list of Guardian articles 1 by 1
for g in guardian_links:

	# Get ID of article we pulled
	id_ = g['response']['content']['id']

	# Get list of related stories as defined by Guardian
	related_list = []
	related = g['response']['relatedContent']
	for r in related:
		related_list.append(r['id'])
	articles[id_]['related_content'] = related_list

	# Get list of story packages as defined by Guardian
	story_package_list = []
	story_package = g['response']['storyPackage']
	for s in story_package:
		story_package_list.append(s['id'])
	articles[id_]['story_package'] = story_package_list


for id_ in articles:
	if 'related_content' not in articles[id_]:
		articles[id_]['related_content'] = "Not extracted"

	if 'story_package' not in articles[id_]:
		articles[id_]['story_package'] = "Not extracted"

save_pickle(articles, options.current_articles_path)