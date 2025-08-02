import pytest

from bs4 import BeautifulSoup
from src.Scraper.RightMove.page_indexer import Crawler


@pytest.fixture
def crawlerWrapper():
    crawler = Crawler()
    crawler.currPage = "https://www.rightmove.co.uk/house-prices/london.html"

    return crawler 

def testLinkRetrieval(crawlerWrapper):
    expectedResults = [
        "https://www.rightmove.co.uk/house-prices/details/784f4e70-fcaa-40f1-91c7-e69aaa2e3ac9",
        "https://www.rightmove.co.uk/house-prices/details/ed1ef3cd-37dd-45c1-8a70-8fdb18391462",
        "https://www.rightmove.co.uk/house-prices/details/e8879097-923c-4fb0-a985-df7ac894bc96",
        "https://www.rightmove.co.uk/house-prices/details/3d1ea027-7ab6-40db-891b-2f93fa040786",
        "https://www.rightmove.co.uk/house-prices/details/c7678857-78f7-4377-875e-d79eeebf1868"
    ]

    actualResults = crawlerWrapper.getLinksFromPage(crawlerWrapper.currPage)
    
    for expected in expectedResults:
        assert expected in actualResults


def testPageIncrementer(crawlerWrapper):
    startUrl = "https://www.rightmove.co.uk/house-prices/london.html?pageNumber=1"
    nextUrl = "https://www.rightmove.co.uk/house-prices/london.html?pageNumber=2"
    
    fringeCaseUrl = "https://www.rightmove.co.uk/house-prices/london.html"

    # the fringeCaserl is the first url, so when incremented shld return the second one
    assert crawlerWrapper._incrementPageUrl(startUrl) == nextUrl
    assert crawlerWrapper._incrementPageUrl(fringeCaseUrl) == nextUrl

def testStateLoad():
    pass

def testStateSave():
    pass


