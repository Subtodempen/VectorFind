from src.Scraper.queue_handler import queue_handler

from src.Scraper.RightMove.page_indexer import Crawler
from src.Scraper.RightMove.scraper import parseBasicPage

import pytest

@pytest.fixture 
def queueWrapper():
    crawlerObj = Crawler("testQueue.json")
    queueHandler = queue_handler(parseBasicPage, crawlerObj)

    return queueHandler
    
def testQueueHandler(queueWrapper):
    assert queueWrapper.constructQueueHandler(2)


