import pytest

from bs4 import BeautifulSoup
from src.Scraper.RightMove.page_indexer import Crawler

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

def testHtmlGetter(crawlerWrapper):
    testUrl = "https://httpbin.org/html"
    expectedResult = "Herman Melville - Moby-Dick"

    actualResults = crawlerWrapper._getHtml(testUrl)

    assert expectedResult in actualResults
    
    
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
    
