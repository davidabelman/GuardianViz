def cleanDoc(doc):
    stopset = set(stopwords.words('english'))
    stemmer = nltk.PorterStemmer()
    tokens = WordPunctTokenizer().tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    final = [stemmer.stem(word) for word in clean]
    return final

class MyCorpus(object):
    def __iter__(self):
        for line in open('corpus.txt'):
            yield dictionary.doc2bow(line.lower().split())

dictionary = corpora.Dictionary(line.lower().split() for line in open('corpus.txt'))