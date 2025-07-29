from bs4 import BeautifulSoup
from selenium import webdriver

class Crawler:
    def __init__(self):
        self.soupEngine = None
        self.pageList = []

        self.driver = webdriver.Chrome()
    
    # using selenium now but anything can be used
    def get_html(url):
        self.driver.get(url)

        return self.driver.page_source
    
    def initSoupEngine(htmlDoc):
        self.soupEngine = BeautifulSoup(htmlDoc)

    # find all <'a'> attriubuytes with data-testid = propertyCard
    def getLinksFromPage(pageUrl):
        links = soupEngine.find_all(
            'a', attrs={'data-testid': propertyCard}
        )

        return links

