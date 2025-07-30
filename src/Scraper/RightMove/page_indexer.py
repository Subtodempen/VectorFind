from bs4 import BeautifulSoup
import requests

class Crawler:
    def __init__(self):
        self.currPage = None
        self.crawledUrls = []    
    
    def _getHtml(self, url):
        response = requests.get(url)
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
            return pageUrl + indentifier
        
        for i in range(index, index + len(indentifier)):
            prevPageNumber += pageUrl[i]

        pageNumber = int(prevPageNumber) + 1
        return pageUrl.replace(prevPageNumber, str(pageNumber))


    
    def crawlPages(self):
        self.currPage = _incrementPageUrl(self.currPage)

        self.crawledUrls += self.currPage
        return getLinksFromPage(self.currPage)

    def loadCrawlState(self):
        pass

    def saveCrawlState(self):
        pass





