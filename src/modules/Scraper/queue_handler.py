import queue
import threading

import time 

from utils.downloader import getHtml

class queue_handler:
    def __init__(self, pageScraperFunction, crawlerObj):
        self.queue = queue.Queue()
        self.resultsList = []
        
        self.crawler = crawlerObj
        self.pageScraperFunction = pageScraperFunction

    def producer(self, stopFlag):
        while not stopFlag():
         # continuesly loop and append the queue with crawled pages :)
            foundLinks = self.crawler.crawlPage()
            
            if foundLinks is None:
                continue

            for link in foundLinks:
                self.queue.put(link)

    # the producer or crawler will find links of sold houses 
    # then the consumer will scrape them and get a address image duo
    # which is appended to the class interface the resultsList
    def consumer(self, stopFlag):
        while not stopFlag():
            page = self.queue.get()

            if page is None:
                break

            htmlDoc = getHtml(page)
            result = self.pageScraperFunction(htmlDoc)

            self.resultsList.append(result)
    

    def createTaskThread(self, functionObj):
        stopFlag = threading.Event()
        
        thread = threading.Thread(
            target=functionObj, 
            args=(lambda: stopFlag.is_set(),))

        thread.start()

        return stopFlag, thread
        

    




