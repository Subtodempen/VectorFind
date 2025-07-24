import queue

from html_fetcher import get_html

class queue_handler:
    def __init__(self, pageScraperFunction, crawlerObj):
        self.queue = queue.Queue()
        self.resultsList = []
        
        self.crawler = crawlerObj
        self.pageScraperFunction = pageScraperFunction

    def producer(stopFlag):
        while not stopFlag:
            
    
    def consumer(stopFlag):
        while not stopFlag:
            page = queue.get()

            if page is None:
                break

            htmlDoc = self.crawler.get_html(page)
            result = self.pageScraperFunction(htmlDoc)

            resultsList.append(result)

    




