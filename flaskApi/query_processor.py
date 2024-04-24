import math
import pickle
import string
import subprocess
import requests
from flask import Flask, request, jsonify
import sys

from nltk import PorterStemmer, WordNetLemmatizer, edit_distance
from nltk.corpus import stopwords, wordnet

sys.path.append('/Users/maksym/Documents/GitHub/Gamayun/webcrawler/webcrawler/utils')

app = Flask(__name__)


@app.route('/runspider', methods=['POST'])
def run_spider():
    # Specify the path to the spider file
    spider_file_path = '/Users/maksym/Documents/GitHub/Gamayun/webcrawler/webcrawler/spiders/web_pull.py'

    # Run the runspider command
    subprocess.run(['scrapy', 'runspider', spider_file_path])

    return jsonify({'message': 'Spider execution completed successfully'}), 200


@app.route('/query', methods=['POST'])
def process_query():
    # validate query
    query_data = request.get_json()
    if not query_data:
        return jsonify({'error': 'Invalid JSON format'}), 400
    if 'query' not in query_data:
        return jsonify({'error': 'Query field is missing'}), 400

    # retrieve the query from the request
    query = query_data['query']
    tokenized_query = tokenize_query(query)

    # crawl docs to construct idfttdf
    response = requests.post('http://localhost:5000/runspider')

    # if crawling was succesfull
    if response.status_code == 200:
        # load the inverted index from the pickled file
        unpickled = load_index("index.pkl")

        # Retrieve results from the inverted index
        ranked_results = search(tokenized_query, unpickled, 10)
        return jsonify({'results': retrieve_document_contents(ranked_results)}), 200
    else:
        return jsonify({'error': 'Failed to call runspider'}), 500


# difference from doc tokenization is query spelling corrections
def tokenize_query(query):
    stopword = set(stopwords.words('english'))
    punct = set(string.punctuation)
    ps = PorterStemmer()

    all_tokens = []  # in query
    for word in query.split():
        # filter out stopwords and punctuation
        if word.lower() not in stopword and word.lower() not in punct:
            # stem and correct the query term
            token = ps.stem(word.lower())
            #corr_token = spell(token)
            #all_tokens.append(corr_token)
            all_tokens.append(token)
    return all_tokens


def load_index(filename):
    print('unpickling index...')
    with open('/Users/maksym/Documents/GitHub/Gamayun/output/' + filename, "rb") as f:
        index = pickle.load(f)
    return index


def vectorize_query(query_tokens, index):
    ps = PorterStemmer()
    query_vector = {}
    # if stem of the term is present in the index then retrieve its tfidf score, else 0
    for qtoken in query_tokens:
        print(f"corrected q token: {qtoken}")
        stem = ps.stem(qtoken)
        if stem in index:
            query_vector[stem] = index[stem]
        else:
            query_vector[stem] = 0
    return query_vector


def search(query_tokens, tfidf_index, num_results=10):
    # stores the final docids-scores for ranked retrieval
    ranking = {}

    q_vector = vectorize_query(query_tokens, tfidf_index)

    # go through each query term posting
    for query_term, query_idscores in q_vector.items():
        # for each pair of docid and score in postings list for query term
        for posting in tfidf_index.get(query_term, []):
            doc_id, doc_tfidf = posting
            # and for each docid and score in query vector
            for id, s in query_idscores:
                # update/initiate score for that docid
                if doc_id == id:
                    # multiply score from query vector and from
                    # document vector and add to the existing score
                    ranking[doc_id] = ranking.get(doc_id, 0) + s * doc_tfidf

    # stores vector length (magnitude) for each document in vectorized query
    # used to calculate final dot product of query X document
    vector_length = {}
    for q_term in q_vector.keys():
        if q_term in tfidf_index.keys():
            for doc_id, score in tfidf_index[q_term]:
                if doc_id not in vector_length:
                    vector_length[doc_id] = 0
                vector_length[doc_id] += score ** 2

    # take square root of each square root sum
    for doc_id in vector_length:
        ranking[doc_id] = math.sqrt(ranking[doc_id])

    # divide by a corresponding document vector magnitude
    for doc_id in ranking:
        ranking[doc_id] = ranking[doc_id] / vector_length[doc_id]

    # sort the dictionary of ranked docs
    return sorted(ranking.items(), key=lambda x: x[0], reverse=True)


# chooses top 10 most relevant articles and returns them
def retrieve_document_contents(ranked_documents):
    counter = 0;
    ret = []
    og_articles = load_original_articles()
    for doc_id, score in ranked_documents:
        counter = counter + 1
        if doc_id < len(og_articles):
            if counter < 12:
                ret.append(og_articles[doc_id])
            else:
                return ret
    return ret


def load_original_articles():
    print('unpickling original articles')
    with open('/Users/maksym/Documents/GitHub/Gamayun/original/' + "orig_articles", "rb") as f:
        articles = pickle.load(f)
    return articles


if __name__ == '__main__':
    app.run(debug=True)
