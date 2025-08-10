from modules.CLIP import CLIPWrapper
from modules.postgres import postgresWrapper

from modules.Scraper.queue_handler import queue_handler

from modules.Scraper.RightMove.page_indexer import Crawler
from modules.Scraper.RightMove.scraper import parseBasicPage

import logging
import sys

import torch
import numpy as np

from utils.downloader import downloadTempImg

class VectorFindApp:
    def __init__(self):
        self.postgresWrapper = None
        self.taskQueue = None
        self.clipWrapper = None

        logging.getLogger().setLevel(logging.INFO)

    def initTaskQueue(self, jsonSaveFile):
        crawlerObj = Crawler(jsonSaveFile)
        self.taskQueue = queue_handler(parseBasicPage, crawlerObj)

        try:
            self.taskQueue.crawler.JSONHandler.loadCrawlState()

        except Exception as e:
            logging.warn("Could not load scraper state.")

        logging.info("initialised task Queue")

    def initClipWrapper(self):
        try:
            self.clipWrapper = CLIPWrapper("openai/clip-vit-base-patch32")
            self.clipWrapper.initClip()
        
        except Exception as e:
            logging.error("CLIP Could not initialise, due to: %s", e)
            sys.exit()
        
        logging.info("initialised clipWrapper")

    def initDBWrapper(self):
        try:
            self.postgresWrapper = postgresWrapper("vecquery")   
            self.postgresWrapper.loadConfig('../database.ini')   
            self.postgresWrapper.connectToDatabase()

        except Exception as e:
            logging.error("Can not init postgres database due to: %s", e)
            sys.exit()
        
        logging.info("initialised The postgres Database")

    def clipEmbedImage(self, imgPath):
        image = self.clipWrapper.loadImage(imgPath)
        vectorImg = self.clipWrapper.processImage(image)
        embeddedImg = self.clipWrapper.embedImg(vectorImg)

        if embeddedImg is None:
            logging.warning("Image %s", imgPath, "could not be embedded")

        return embeddedImg
    
    def convertTorchToNumPy(self, tensor):
        if tensor is None:
            return None

        tensor32 = tensor.to(torch.float32)
        return tensor32.numpy().tolist()[0]


    def insertEmbeddedImg(self, imgVec, address):
        self.postgresWrapper.bufferedAppend(address, imgVec)
        self.postgresWrapper.flushBuffer()

        self.postgresWrapper.commitTransaction()

    def startScraping(self):
        producerStop, pThread = self.taskQueue.createTaskThread(self.taskQueue.producer)
        consumerStop, cThread = self.taskQueue.createTaskThread(self.taskQueue.consumer)
        
        try:
            while True:
                if len(self.taskQueue.resultsList) != 0:
                    self.processScrapedResults()

                    logging.info("Currently Sraping... press Crtl-C to stop")

        except KeyboardInterrupt:
            pass


        producerStop.set()
        consumerStop.set()

        pThread.join()
        cThread.join()
    
    def processScrapedResults(self):
        scrapeResult = self.taskQueue.resultsList.pop()
        
        if scrapeResult is None:
            return

        address = scrapeResult[0]
        imageLinks = scrapeResult[1]

        for i in imageLinks:
            # download image 
            imgPath = downloadTempImg(i)
                
            # than append the pil object straight to CLIP 
            tensor = self.clipEmbedImage(imgPath.name)
                
            # than convert it to a numpy object
            imgVec = self.convertTorchToNumPy(tensor)

            # than append it, with the address to the postgres db 
            self.postgresWrapper.bufferedAppend(address.text, imgVec)

            # close temp image
            imgPath.close()
        
        self.postgresWrapper.commitTransaction()
        logging.info("succsesfuly proccessed: %s", address)


    
app = VectorFindApp()
app.initTaskQueue("test.json")
app.initClipWrapper()
app.initDBWrapper()


app.startScraping()

app.postgresWrapper.closeConnection()
app.taskQueue.crawler.JSONHandler.loadCrawlState()

logging.info("EXITED GRACEFULLY")
#print( imgVec) 

#app.insertEmbeddedImg(imgVec, "thgis is another owl")
