import pickle

import scrapy
import json

from webcrawler.webcrawler.utils.indexer import Indexer


class WebCrawler(scrapy.Spider):
    name = "webcrawler"

    # Initialize using seed URL/Domain, Max Pages, Max Depth
    def __init__(self, seed_url=None, max_pages=100, max_depth=3, *args, **kwargs):
        print('init webcrawler')
        super().__init__(*args, **kwargs)
        self.articles = []
        self.documents = []
        self.indexer = Indexer()
        self.start_urls = [seed_url] if seed_url else []
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited_urls = set()

    def start_requests(self):
        print('starting requests')
        urls = [
            'https://newsapi.org/v2/everything?q=car&sortBy=popularity&apiKey=37795d274a33458dafa80ff7ec8302cb',
            'https://newsapi.org/v2/everything?q=house&sortBy=popularity&apiKey=37795d274a33458dafa80ff7ec8302cb',
            'https://newsapi.org/v2/everything?q=tree&sortBy=popularity&apiKey=37795d274a33458dafa80ff7ec8302cb',

        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('parsing...')
        # check if max num of pages was reached
        if len(self.documents) >= self.max_pages:
            return

        # visited url
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)

        # get the json response body
        data = json.loads(response.body)
        articles = data.get("articles", [])
        self.articles = articles
        self.pickle_original_articles(self.articles)

        for article in articles:
            content = article.get("content", "")
            if content:
                self.documents.append(content)

        # construct tfidf index will automatically pickle in output folder
        self.indexer.tfidf(self.documents)

    def close(self, reason='crawling DONE!'):
        print('closing')
        # when the crwaling is done then index can be constcuted
        self.indexer.tfidf(self.documents)
        print(self.indexer.load_index('index.pkl'))
        super().close(self, reason)

    def pickle_original_articles(self, articles):
        print('pickling original articles')
        with open('/Users/maksym/Documents/GitHub/Gamayun/original/' + "orig_articles", "wb") as f:
            pickle.dump(self.articles, f)

