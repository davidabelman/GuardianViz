"""
pipeline.py
"""

import opencrawl
reload(opencrawl)
import opencrawl_wrangle


pipeline = [
				#opencrawl, 				# Crawls Guardian articles to get main info available (not related stories)
				#opencrawl_wrangle,  		# Cleans the Guardian article data into dictionary format
				#facebook_crawl,  			# Pulls FB share data for articles
				#facebook_wrangle,			# Adds FB data to overall pickle
				#guardian_link_crawl,		# Crawls info on related stories etc.
				#guardian_link_wrangle,		# Adds Guardian related stories data to overall pickle
			]


def main(pipeline):
	""" Call the specified list of steps in the pipeline """
	for module in pipeline:
		module.main()

if __name__ == main(pipeline):
	sys.exit(main())