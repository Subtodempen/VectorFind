import torch
from PIL import Image
from transformers import AutoModel, AutoProcessor

from pathlib import Path
import logging 

class CLIPWrapper:
    def __init__(self, modelName):
        self.__modelName__ = modelName
        self.model = None
        self.processor = None
 
    # define the processor and model
    def initClip(self):
        self.model = AutoModel.from_pretrained(self.__modelName__, 
                                               torch_dtype=torch.bfloat16, 
                                               attn_implementation="sdpa")
        
        self.processor = AutoProcessor.from_pretrained(self.__modelName__)
        

    def loadImage(self, imagePath):
        if not Path(imagePath).is_file():
            logging.warning("could not open " + imagePath) 
            return None
        
        image = Image.open(imagePath)
        return image
        
    def processImage(self, img):
        try:
            input = self.processor(
                images = img,
                return_tensors="pt", 
                padding=True
            )

            return input
            
        except Exception as e:
            logging.error("Failure to process image: %s", e)
            return None

    def embedImg(self, imgVector):
        if imgVector is None:
            logging.error("No image present")
            return None

        try:
            with torch.no_grad():
                features = self.model.get_image_features(**imgVector)
            return features
        
        except Exception as e:
            logging.error("can not embed vector image: %s", e)
            return None
    
