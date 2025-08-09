from CLIP import CLIPWrapper
from postgres import postgresWrapper

from Scraper.queue_handler import queue_handler

from Scraper.RightMove.page_indexer import Crawler
from Scraper.RightMove.scraper import parseBasicPage

import logging
import sys

import torch
import numpy as np

class VectorFindApp:
    def __init__(self):
        self.postgresWrapper = None
        self.taskQueue = None
        self.clipWrapper = None

    def initTaskQueue(self, jsonSaveFile):
        crawlerObj = Crawler(jsonSaveFile)
        self.taskQueue = queue_handler(parseBasicPage, crawlerObj)

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
            logging.warning("Image", path, "could not be embedded")

        return embeddedImg
    
    def convertTorchToNumPy(self, tensor):
        tensor32 = tensor.to(torch.float32)
        return tensor32.numpy().tolist()[0]


    def insertEmbeddedImg(self, imgVec, address):
        self.postgresWrapper.bufferedAppend(address, imgVec)
        self.postgresWrapper.flushBuffer()

        self.postgresWrapper.commitTransaction()


    
app = VectorFindApp()
app.initTaskQueue("test.json")
app.initClipWrapper()
app.initDBWrapper()

tensor = app.clipEmbedImage("owl.png")
imgVec = app.convertTorchToNumPy(tensor)

#print( imgVec) 

#app.insertEmbeddedImg(imgVec, "thgis is another owl")
print(app.postgresWrapper.getClosestVec(imgVec))
