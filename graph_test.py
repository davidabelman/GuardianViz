"""
Testing graphing capabilities
"""

import pickle
import options
reload(options)
from general_functions import *
import networkx as nx

articles = load_pickle(options.articles_uk_path)

# import networkx
G=nx.Graph()

# build up the graph (try different things - facebook likes, internal connections, related stories, story packages, tags, etc.)
for _id in articles:
	G.add_node(_id, headline=articles[_id]['headline'])

	a = articles[_id]

for id_a in articles:
	a = articles[id_a]
	if type(a['related_content']) == list:
		for id_b in a['related_content']:
			if id_b in articles:
				G.add_edge(id_a,id_b)


# # try for different subsets of the graph
# # export as graphml and plot in gephi
# pr = nx.pagerank(G, alpha=0.9)
# l=[]
# for i in pr:
#     l.append((pr[i],i))
# l.sort(reverse=True)
# for item in l[0:40]:
# 	print item

nx.write_graphml(G, "test.graphml")