from src.modules.Scraper.queue_handler import queue_handler

from src.modules.Scraper.RightMove.page_indexer import Crawler
from src.modules.Scraper.RightMove.scraper import parseBasicPage

import pytest

@pytest.fixture 
def queueWrapper():
    crawlerObj = Crawler("test_queue.json")
    queueHandler = queue_handler(parseBasicPage, crawlerObj)

    return queueHandler
    


