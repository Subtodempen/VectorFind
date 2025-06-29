from CLIP import CLIPWrapper

clip = CLIPWrapper("openai/clip-vit-base-patch32")


clip.initCLIP()
image = clip.loadImage("Moon.png")
imageVec = clip.processImage(image);

print(clip.embedImage(imageVec))
