from CLIP import CLIPWrapper
from postgres import postgresWrapper 

def initCLIPWrapper()
    clip = CLIPWrapper("openai/clip-vit-base-patch32")
    clip.initCLIP()
    
    return clip

def initDBWrapper():
    db = postgresWrapper("vecquery")   
    db.loadConfig('../database.ini')   
    db.connectToDatabase()

    return db    

if __name__ == "__main__":
    initCLIPWrapper()
    initDBWrapper()
    
