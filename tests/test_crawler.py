import pytest

from bs4 import BeautifulSoup
from src.modules.Scraper.RightMove.page_indexer import Crawler

import json

@pytest.fixture
def crawlerWrapper():
    crawler = Crawler(None)
    crawler.currPage = "https://www.rightmove.co.uk/house-prices/london.html"

    return crawler 

@pytest.fixture
def crawlerStateWrapper():
    return Crawler("test.json")

def testLinkRetrieval(crawlerWrapper):
    expectedResults = "https://www.rightmove.co.uk/house-prices/details/"

    actualResults = crawlerWrapper.getLinksFromPage(crawlerWrapper.currPage)
    
    for link in actualResults:
        assert expectedResults in link


def testPageIncrementer(crawlerWrapper):
    startUrl = "https://www.rightmove.co.uk/house-prices/london.html?pageNumber=1"
    nextUrl = "https://www.rightmove.co.uk/house-prices/london.html?pageNumber=2"
    
    fringeCaseUrl = "https://www.rightmove.co.uk/house-prices/london.html"

    # the fringeCaserl is the first url, so when incremented shld return the second one
    assert crawlerWrapper._incrementPageUrl(startUrl) == nextUrl
    assert crawlerWrapper._incrementPageUrl(fringeCaseUrl) == nextUrl

def testStateSave(crawlerStateWrapper):
    expectedResult = "SAVE TEST URL"
    testFile = crawlerStateWrapper.JSONHandler.jsonFName
        
    crawlerStateWrapper.currPage = expectedResult
    crawlerStateWrapper.crawledPages = []
    
    crawlerStateWrapper.JSONHandler.saveCrawlState()

    # open json file and try and find the expectedResul at currUrl
    with open(testFile, mode="r", encoding="utf-8") as jsonFile:
        rawJson = json.load(jsonFile)

        assert rawJson["currPage"] == expectedResult


def testStateLoad(crawlerStateWrapper):
    expectedResult = "LOAD TEST URL" 
    testFile = crawlerStateWrapper.JSONHandler.jsonFName
    
    crawlerStateWrapper.currPage = expectedResult
    crawlerStateWrapper.crawledPages = []

    # save the classes state
    crawlerStateWrapper.JSONHandler.saveCrawlState()
    
    # reset the classes state
    crawlerStateWrapper.currPage = None
    
    # load the classes state
    crawlerStateWrapper.JSONHandler.loadCrawlState()
    
    # Asserting that the proccess was succseful
    assert crawlerStateWrapper.currPage == expectedResult
    
