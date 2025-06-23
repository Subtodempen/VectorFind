import torch
from PIL import Image
from transformers import AutoModel, AutoProcessor

import os.path
import logging 

class CLIPWrapper:
    def __init__(self, modelName):
        self.__modelName__ = modelName
    
    # define the processor and model
    def initCLIP(self):
        self.model = AutoModel.from_pretrained(self.__modelName__, 
                                               torch_dtype=torch.bfloat16, 
                                               attn_implementation="sdpa")
        
        self.processor = AutoProcessor.from_pretrained(self.__modelName__)

    def loadImage(self, imagePath):
        if not os.path.isfile(imagePath):
            logging.warning("could not open ", imagePath) 
            return
        
        image = Image.open(imagePath)
        return image
        
    def processImage(self, img):
        try:
            input = self.processor(
                images = img,
                return_tensors="pt", 
                padding=True
            )
            
        except:
            logging.error("Failure to process image")

        return input

    def embedImage(self, imgVector):
        try:
            with torch.no_grad():
                features = self.model.get_image_features(**imgVector)
        
        except:
            logging.error("can not embed vector image")

        return features
    
