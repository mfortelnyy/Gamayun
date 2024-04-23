# Gamayun Search Engine

## Abstract
The project aimed to develop a search engine using web crawling and information retrieval techniques. The objectives were to crawl web content, index documents, process user queries, and return relevant search results. The next steps involve improving search accuracy, scalability, and user experience.

## Overview
The solution consists of two main components: a web crawler and a query processor. The web crawler, implemented using Scrapy, retrieves web pages, extracts text content, and indexes documents. The query processor handles user queries, tokenizes them, retrieves relevant documents from the index, and returns search results.

## Design
The system allows users to submit queries through an API endpoint. The query processor tokenizes queries, corrects spelling, retrieves relevant documents from the index, and returns search results. The web crawler extracts text content from web pages, indexes documents, and stores them for retrieval. Both whole original articles and index are pickled.

## Architecture
The software components include the web crawler, query processor, and indexer. The web crawler interacts with web pages, extracts content, and sends it to the indexer. The query processor receives user queries, processes them, and retrieves relevant documents from the indexer. Before querying, webcrawler always perform scrapping and pickles the index. 

## Operation
To run the system, the user can send queries to the query processor API endpoint. The web crawler can be triggered manually or scheduled to run periodically. Installation involves setting up dependencies, such as Scrapy, NLTK, and Flask.

## Conclusion
The project successfully implemented a basic search engine using web crawling and information retrieval techniques. However, there are opportunities for improvement in search accuracy, scalability, and user interface. Future work includes integrating more advanced algorithms, optimizing performance, and enhancing the user experience.

## Data Sources
Data sources include web pages crawled by the web crawler. Additional data sources can be integrated to improve search coverage and relevance.

## Test Cases
Test cases involve verifying the functionality of the web crawler, query processor, and indexer. 
1. Crawl newsapi.org for 'SMCI' and 'NVDIA'
![image](https://github.com/mfortelnyy/Gamayun/assets/78120259/06d5255b-39ef-42f7-bb01-023ea9f9cc09)

 query for 'triple' + get relevant doceument contents
![image](https://github.com/mfortelnyy/Gamayun/assets/78120259/16c763b9-d19d-4653-8396-14c9dea1ecc2)



2. Crawl for 'London', 'Chicago', 'Tesla', 'Musk, 'China'
   ![image](https://github.com/mfortelnyy/Gamayun/assets/78120259/ea992dfe-cf17-459c-b138-ffab560cf879)

   query for 'London Tesla' 
   ![image](https://github.com/mfortelnyy/Gamayun/assets/78120259/b10830cf-c644-4ef6-b95e-26a6c8640695)

3. Crawl for 'ChatGPT', 'car', 'electric'
   ![image](https://github.com/mfortelnyy/Gamayun/assets/78120259/6ec16d9b-70eb-4788-991f-0fb0a873aa7c)

   query for 'engine'
   ![image](https://github.com/mfortelnyy/Gamayun/assets/78120259/2b2c05bc-f2c3-4764-8381-2792d338cdf6)

4. Spelling Correction


## Source Code
The project source code is available in the provided codebase. It includes modules for the web crawler, query processor, indexer, and API endpoints. Dependencies include Scrapy, NLTK, Flask, and Gensim.

## Bibliography
- [Scrapy Documentation](https://docs.scrapy.org/en/latest/)
- [Crawler guide](https://www.zenrows.com/blog/web-crawler-python)
- [Word Embedding](https://www.geeksforgeeks.org/python-word-embedding-using-word2vec/)
- [Postman for teting APIs](https://web.postman.co/workspace/My-Workspace~795e98e5-7950-4bb6-883b-5b883014927d/request/32798101-91ffd987-7f3d-47db-9e37-d9b957ac0e14?tab=body)

### Models Used
- **Scrapy:** A web crawling framework used to extract text content from web pages.
- **NLTK (Natural Language Toolkit):** Utilized for tokenization, spelling correction, and text processing.
- **Flask:** Powers the API endpoints for receiving and processing user queries.
- **Gensim:** Used for implementing the Word2Vec model, which can potentially enhance search results by capturing semantic similarities between words.

### Search Process
1. **Web Crawling:** The web crawler, implemented with Scrapy, visits web pages, extracts text content, and indexes documents.
2. **Indexing:** Extracted text content is processed and indexed using the TF-IDF (Term Frequency-Inverse Document Frequency) technique. This allows for efficient retrieval of relevant documents based on user queries.
3. **Query Processing:** User queries are received through API endpoints. The query processor tokenizes queries, corrects spelling errors, retrieves relevant documents from the index, and ranks them based on relevance.
4. **Search Results:** Ranked search results (whole articles) are returned to the user, providing relevant documents based on the input query.
