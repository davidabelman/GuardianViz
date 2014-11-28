"""
Finds basic cosine similarity between articles based on tags only, and stores this data
Uses: http://stackoverflow.com/questions/15173225/how-to-calculate-cosine-similarity-given-2-sentence-strings-python
"""
import pickle
import options
reload(options)
from general_functions import *

import re, math
from collections import Counter


def get_cosine(vec1, vec2):
    """
    Gets cosine similarity between 2 dicts
    """
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def convert_list_to_dict(list):
    """
    Converts list into dictionary of counts
    """
    dict_to_return = {}
    for l in list:
        if l in dict_to_return:
            dict_to_return[l] += 2
        else:
            dict_to_return[l] = 2
    return dict_to_return

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

WORD = re.compile(r'\w+')
articles = load_pickle(options.path_choice['sample'])

for id_ in articles:
    articles[id_]['tag_similarities'] = {}
    a = articles[id_]
    tags_a = convert_list_to_dict(a['tags'])
    standfirst_a = text_to_vector(a['standfirst'])
    headline_a = text_to_vector(a['headline'])
    a_vector = dict(tags_a.items())
    a_vector = dict(tags_a.items() + headline_a.items())
    #a_vector = dict(tags_a.items() + headline_a.items() + standfirst_a.items())
    temp_similarities = []
    for id2_ in articles:
        b = articles[id2_]
        tags_b = convert_list_to_dict(b['tags'])
        standfirst_b = text_to_vector(b['standfirst'])
        headline_b = text_to_vector(b['headline'])
        b_vector = dict(tags_b.items())
        b_vector = dict(tags_b.items() + headline_b.items())
        #b_vector = dict(tags_b.items() + headline_b.items() + standfirst_b.items())
        similarity = get_cosine(a_vector, b_vector)
        temp_similarities.append((similarity,id2_))
    temp_similarities.sort(reverse=True)
    articles[id_]['tag_similarities'] = temp_similarities[1:6]

        # if similarity>=0.3 and similarity<=.99:
        #     articles[id_]['tag_similarities'][id2_]=similarity

for a in articles:
    print articles[a]['id']
    print "---"
    for x in articles[a]['tag_similarities']:
        print x
    print "\n\n"
