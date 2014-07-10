"""
Testing graphing capabilities
"""

import pickle
import options
reload(options)
from general_functions import *

def split_lines(text):
	"""
	Adds a line break every 2 words in a string of text
	"""
	end, count = "", 0
	split = text.split()
	for w in split:
		count+=1
		end += w
		if count%2==0:
			end += "\n"
		else:
			end += " "
	return end

# Load articles
articles = load_pickle(options.current_articles_path)

# import networkx
import networkx as nx
G=nx.Graph()

# build up the graph (try different things - facebook likes, internal connections, related stories, story packages, tags, etc.)
for _id in articles:
	G.add_node	( 	_id, 
					headline=split_lines(articles[_id]['headline']),
				)
	# try:
	# 	G[_id]['tag'] = articles[_id]['tags'][0]
	# except:
	# 	G[_id]['tag'] = 'Misc'
	a = articles[_id]

for id_a in articles:
	a = articles[id_a]
	if type(a['related_content']) == list:
		for id_b in a['related_content']:
			if id_b in articles:
				G.add_edge(id_a,id_b, weight=0.9)
	if type(a['tfidf_body']) == list:
		for (weight, id_b) in a['tfidf_body']:
			if id_b in articles:
				G.add_edge(id_a,id_b, weight=round(weight,2))


# # try for different subsets of the graph
# # export as graphml and plot in gephi
# pr = nx.pagerank(G, alpha=0.9)
# l=[]
# for i in pr:
#     l.append((pr[i],i))
# l.sort(reverse=True)
# for item in l[0:40]:
# 	print item

nx.write_graphml(G, "test2.graphml")