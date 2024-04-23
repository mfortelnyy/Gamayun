import unittest
from unittest.mock import MagicMock
from webcrawler.spiders.web_pull import WebCrawler

class TestWebCrawler(unittest.TestCase):
    def test_parse(self):
        response = MagicMock()
        response.meta = {'depth': 0}  # Set up meta attribute with depth
        var = '''{
                   "status": "ok",
                   "totalResults": 50973,
                   "articles": [
                       {
                           "source": {
                               "id": null,
                               "name": "[Removed]"
                           },
                           "author": null,
                           "title": "[Removed]",
                           "description": "[Removed]",
                           "url": "https://removed.com",
                           "urlToImage": null,
                           "publishedAt": "1970-01-01T00:00:00Z",
                           "content": "[Removed]"
                       }
                   ]
               }'''
        response.body = var

        webcrawler = WebCrawler()

        webcrawler.parse(response)

        # Assert that the parse method is called and documents are appended
        #self.assertTrue(webcrawler.documents)
        #self.assertEqual(len(webcrawler.documents), 1)
        #self.assertEqual(webcrawler.documents[0], "[Removed]")  # Assuming this is the content

if __name__ == '__main__':
    unittest.main()
