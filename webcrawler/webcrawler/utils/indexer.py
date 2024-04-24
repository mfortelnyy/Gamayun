import pickle
import math
import re
import string

from nltk import PorterStemmer
from nltk.corpus import stopwords


class Indexer:
    def __init__(self):
        self.index = {}
        self.doc_lengths = {}
        self.model = None

    @staticmethod
    def tokenize(self, document):
        stopword = set(stopwords.words('english'))
        punct = set(string.punctuation)
        ps = PorterStemmer()

        all_tokens = []  # per doc
        for word in document.split():
            clean_word = re.sub(r'[^\w\s]', '', word)
            # filter out stopwords and punctuation
            if clean_word.lower() not in stopword and clean_word.lower() not in punct and len(clean_word) != 0:
                # save stemmed token
                token = ps.stem(clean_word.lower())
                all_tokens.append(token)
        return all_tokens

    def tfidf(self, docs):
        print('indexing....')
        # stores a dictionary {<term>: <[docIDs:termFreq], docFreq>}
        doc_freq_dict = {}
        docs_N = 0

        # iterate over collection and calc doc freq (num of docs particular term appears)
        for docID, document in enumerate(docs):
            current_doc_terms = set()
            # print(f'docID: {docID}, doc content: {document}')
            tokens = self.tokenize_document(self, document)
            # print(tokens)

            for term in tokens:
                # print(term)
                # if term is in dict then mark as present and increase counter by
                # one and add docID to postings, if not - initialize the value
                if term in doc_freq_dict:
                    # print(f'term {term} is in doc freq dict')
                    # if term is already seen in a document update the term freq accrodingly
                    if term in current_doc_terms:
                        # retrieve current postings for the term from dict
                        doc_ids, doc_freq = doc_freq_dict[term]
                        term_freq_in_doc = doc_ids[docID]
                        doc_ids[docID] = term_freq_in_doc + 1
                        doc_freq_dict[term] = (doc_ids, doc_freq)
                    else:
                        # retrieve current postings for the term from dict
                        doc_ids, doc_freq = doc_freq_dict[term]
                        # create a new entry for docID:term dict
                        doc_ids[docID] = 1
                        # update and assign a new tuple
                        doc_freq_dict[term] = (doc_ids, doc_freq + 1)
                    # print(f'term {term} has  doc freq {doc_freq}')
                if term not in doc_freq_dict:
                    doc_freq_dict[term] = ({docID: 1}, 1)
                # only unique terms
                current_doc_terms.add(term)

            # accounts for start of counter - 0
            docs_N = docID + 1

        # now construct index by calculating tfidf for each term
        tf_idf_index = {}
        for term, postings in doc_freq_dict.items():
            tf_idf_index[term] = []
            doc_freq = postings[1]
            for doc_id, termFreq in postings[0].items():
                idf = math.log(docs_N / doc_freq, 10)
                score = idf * termFreq
                # print(f"score for : '{term}' with score {score}")
                tf_idf_index[term].append((doc_id, score))
                #print(tf_idf_index[term])
        self.index = tf_idf_index
        # print(tf_idf_index['smci'])
        #print(self.index)
        self.pickle_index("index.pkl")
        return tf_idf_index, docs_N

    def pickle_index(self, filename):
        print('pickling index')
        with open('/Users/maksym/Documents/GitHub/Gamayun/output/' + filename, "wb") as f:
            print(self.index)
            pickle.dump(self.index, f)

    @staticmethod
    def tokenize_document(self, document):
        stopword = set(stopwords.words('english'))
        punct = set(string.punctuation)
        ps = PorterStemmer()

        all_tokens = []  # per doc
        for word in document.split():
            clean_word = re.sub(r'[^\w\s]', '', word)
            # filter out stopwords and punctuation
            if clean_word.lower() not in stopword and clean_word.lower() not in punct and len(clean_word) != 0:
                # save stemmed token
                token = ps.stem(clean_word.lower())
                all_tokens.append(token)
        return all_tokens

    def load_index(self, filename):
        print('unpickling')
        with open('/Users/maksym/Documents/GitHub/Gamayun/output/' + filename, "rb") as f:
            self.index = pickle.load(f)

    def word2vec_model(self, documents, vector_size=100, window=5, min_count=1, workers=4):
        corpus = [self.tokenize_document(self, document) for document in documents]
        from gensim.models import Word2Vec
        self.model = Word2Vec(corpus, vector_size=vector_size, window=window, min_count=min_count, workers=workers)
