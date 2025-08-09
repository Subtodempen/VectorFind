import queue
import threading


import time 


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

        
    def consumer(self, stopFlag):
        while not stopFlag():
            page = self.queue.get()

            if page is None:
                break

            htmlDoc = self.crawler._getHtml(page)
            result = self.pageScraperFunction(htmlDoc)

            self.resultsList.append(result)

    def constructQueueHandler(self, n):
        # n is the ratio of consumers per producer in n : 1
        self.crawler.JSONHandler.loadCrawlState()

        stopFlag1 = threading.Event()
        stopFlag2 = threading.Event()
        
        producerThread = threading.Thread(target=self.producer, args=(lambda: stopFlag1.is_set(),))
        consumerThread = threading.Thread(target=self.consumer, args=(lambda: stopFlag2.is_set(),))

        producerThread.start()
        consumerThread.start()
        
        time.sleep(5)
        

        stopFlag1.set()
        stopFlag2.set()

        producerThread.join()
        consumerThread.join()


        self.crawler.JSONHandler.saveCrawlState()

        return True
            

    




