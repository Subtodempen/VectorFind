import torch
from PIL import Image
from transformers import AutoModel, AutoProcessor


class CLIPWrapper:
    def __init__(self, modelName):
        self.__modelName__ = modelName
    
    # define the processor and model
    def initCLIP(self):
        self.model = AutoModel.from_pretrained(self.__modelName__, 
                                               torch_dtype=torch.bfloat16, 
                                               attn_implementation="sdpa")
        
        self.processor = AutoProcessor.from_pretrained(self.__modelName__)
