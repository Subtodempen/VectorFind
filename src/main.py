from CLIP import CLIPWrapper
from postgres import postgresWrapper 


if __name__ == "__main__":
    db = postgresWrapper()    
    db.loadConfig('../database.ini')   
    db.connectToDatabase()

    #clip = CLIPWrapper("openai/clip-vit-base-patch32")

    #clip.initCLIP()
    #image = clip.loadImage("Moon.png")
    #imageVec = clip.processImage(image);

    #print(clip.embedImage(imageVec))

    
