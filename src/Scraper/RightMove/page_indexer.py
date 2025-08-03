from bs4 import BeautifulSoup

import requests
from requests.adapters import HTTPAdapter, Retry

import logging


class Crawler:
    def __init__(self):
        self.crawledUrls = []   
        self.currPage = None

    def _getHtml(self, url):
        session = requests.Session()
        
        # construct a request tiemout loop and try 5 more 
        MAX_RETRY = 5
        BACK_OFF = 1
        ERROR_CODES = [500, 502, 504]

        retries = Retry(
            total=MAX_RETRY, 
            backoff_factor=BACK_OFF,
            status_forcelist=ERROR_CODES
        )
            

        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('http://', HTTPAdapter(max_retries=retries))

        try:
            response = session.get(url)

        except requests.exceptions.TooManyRedirects:
            logging.warning("invalid URL, base crawler URL is invalid")
            return None

        except requests.exceptions.RequestException as e:
            logging.error("Catostrophic request error" + e)
            return None
        
        return response.text
           
    def _initSoupEngine(self, htmlDoc):
        return BeautifulSoup(htmlDoc)

    # find all <'a'> attriubuytes with data-testid = propertyCard
    def getLinksFromPage(self, pageUrl):
        htmlDoc = self._getHtml(pageUrl)
        soupEngine = self._initSoupEngine(htmlDoc)

        parsedLinks = []

        linkAttr = soupEngine.find_all(
            'a', attrs={'data-testid': 'propertyCard'}
        )
        
        for linkA in linkAttr:
            parsedLinks.append(linkA['href'])
        
        return parsedLinks
    
    def _incrementPageUrl(self, pageUrl):
        # find ?pageNumber in the url, if not present then append it to url 
        indentifier = '?pageNumber='
        index = pageUrl.find(indentifier)

        if index == -1:
            secondPageIndex = '2'
            return pageUrl + indentifier + secondPageIndex # if no ?pageNumber index then go to second page
        
        prevPageNumber = pageUrl[index + len(indentifier)]
    
        nextPageNumber = int(prevPageNumber) + 1
        return pageUrl.replace(prevPageNumber, str(nextPageNumber))

    
    def crawlPages(self):
        self.currPage = _incrementPageUrl(self.currPage)

        self.crawledUrls += self.currPage
        return getLinksFromPage(self.currPage)

    def loadCrawlState(self):
        pass

    def saveCrawlState(self):
        pass





