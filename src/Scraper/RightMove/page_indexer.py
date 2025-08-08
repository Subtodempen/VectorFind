from bs4 import BeautifulSoup

import requests
from requests.adapters import HTTPAdapter, Retry

import logging
import json

class JSONHandler:
    def __init__(self, crawlerStateClass, fName):
        self.jsonFName = fName
        self.crawlerState = crawlerStateClass
        
    def fileErrorHandle(fileFunc):
        def tryExcept(self):     
            try:
                fileFunc(self)    
        
            except FileNotFoundError:
                logging.warning("Can not find JSON save file, file not found.")

            except PermissionError:
                logging.warning("Do not have permission to access file.")

            except Exception as e:
                logging.warning("File not saved to, can not save state. Due to: %s", e)
        
        return tryExcept

    @fileErrorHandle
    def loadCrawlState(self):
        with open(self.jsonFName, mode='r', encoding="utf-8") as jsonRead:
            rawJson = json.load(jsonRead)
        
        self.crawlerState.currPage = rawJson["currPage"]
        self.crawlerState.crawledPages = rawJson["crawledPages"]
    
    @fileErrorHandle
    def saveCrawlState(self): 
        jsonFormat = {
            "currPage": self.crawlerState.currPage,
            "crawledPages": self.crawlerState.crawledPages
        }

        with open(self.jsonFName, mode='w', encoding='utf-8') as jsonWrite:
            json.dump(jsonFormat, jsonWrite) 
       

class Crawler:
    def __init__(self, jsonFName):
        self.currPage = None
        self.crawledPages = []

        if jsonFName is None:
            self.JSONHandler = None  

        else:
            self.JSONHandler = JSONHandler(self, jsonFName)
        
    
    def _getHtml(self, url):
        session = requests.Session()
        genericHeader = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }        

        # construct a request tiemout loop and try 5 more 
        MAX_RETRY = 5
        BACK_OFF = 1
        ERROR_CODES = [500, 502, 504]
        TIMEOUT = 10

        retries = Retry(
            total=MAX_RETRY, 
            backoff_factor=BACK_OFF,
            status_forcelist=ERROR_CODES
        )
            

        session.mount('http://', HTTPAdapter(max_retries=retries))

        try:
            response = session.get(url, timeout=TIMEOUT, headers=genericHeader)

        except requests.exceptions.TooManyRedirects:
            logging.warning("invalid URL, base crawler URL is invalid")
            return None

        except requests.exceptions.RequestException as e:
            logging.error("Catostrophic request error: %s", e)
            return None
        
        return response.text
           
    def _initSoupEngine(self, htmlDoc):
        return BeautifulSoup(htmlDoc, "html.parser")

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

    
    def crawlPage(self):
        if self.currPage is None:
            logging.error("JSON state has not been loaded")
            return None
        
        self.currPage = self._incrementPageUrl(self.currPage)
        foundLinks = self.getLinksFromPage(self.currPage)
        
        # make sure pageLinks have not already been crawled 
        for link in foundLinks:
            if link in self.crawledPages:
                # link has allready been crawled
                foundLinks.remove(link) 
        
        self.crawledPages += foundLinks
        return foundLinks 


