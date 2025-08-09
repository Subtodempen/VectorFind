from CLIP import CLIPWrapper
from postgres import postgresWrapper 

import torch
import argparse

def initCLIPWrapper():
    clip = CLIPWrapper("openai/clip-vit-base-patch32")
    clip.initCLIP()
    
    return clip

def initDBWrapper():
    db = postgresWrapper("vecquery")   
    db.loadConfig('../database.ini')   
    db.connectToDatabase()

    return db    

def processAndEmbedImage(CLIPWrapper, path):
    image = CLIPWrapper.loadImage(path)
    vectorImg = CLIPWrapper.processImage(image)    
    embeddedImg = CLIPWrapper.embedImage(vectorImg)

    return embeddedImg

def convertTorchToNumPy(tensor):
    tensor32 = tensor.to(torch.float32)
    return tensor32.numpy().tolist()[0]

def insertAddressVec(dbWrapper, imageVec, address):
    dbWrapper.bufferedAppend(imageVec, address)
    dbWrapper.flushBuffer()

    dbWrapper.commitTransaction()


if __name__ == "__main__":
    CLIPWrapper = initCLIPWrapper()
    dbWrapper = initDBWrapper()

    argParser = argparse.ArgumentParser()
    argParser.add_argument("imageFile")
    argParser.add_argument("address")
    
    argParser.add_argument("-a", "--add", action="store_true")
    argParser.add_argument("-q", "--query", action="store_true")

    args = argParser.parse_args()
    
    tensor = processAndEmbedImage(CLIPWrapper, args.imageFile)
    imageVec = convertTorchToNumPy(tensor)
     
    if args.add:
        # processImage
        # Then we append to the database   
        insertAddressVec(dbWrapper, args.address, imageVec)
        
    elif args.query:
        # or we can query an image....
        # so search the database for nearest vec querys to the image
        closest = dbWrapper.getClosestVec(imageVec)
        

