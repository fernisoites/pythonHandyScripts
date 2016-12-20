from PIL import Image
from PIL import ImageDraw, ImageFont
import sys

class rectangle():
    def __init__(self,width,height):
        self.height=height
        self.width=width
        self.left=0
        self.right=self.left+width
        self.up=0
        self.down=self.up+height
        self.lu=[self.left,self.up]
        self.ld=[self.left,self.down]
        self.ru=[self.right,self.up]
        self.rd=[self.right,self.down]

    def locate(self,left,up):
        self.up=up
        self.left=left
        self.down=self.up+self.height
        self.right=self.left+self.width
        self.lu=[self.left,self.up]
        self.ld=[self.left,self.down]
        self.ru=[self.right,self.up]
        self.rd=[self.right,self.down]

filename = sys.argv[1]
singleImage = Image.open(filename)
singleWidth , singleHeight = singleImage.width , singleImage.height

pic=rectangle(int(singleHeight * 3.1), int(singleHeight*2.05))

im=Image.new("RGB",(pic.width,pic.height), "white")

draw=ImageDraw.Draw(im)

offset = (singleHeight - singleWidth)/2.0
space = singleHeight*0.05


for i in range(2):
    for j in range(3):
        left = offset * (j*2+1) + (singleWidth+space) * j
        right = left + singleWidth
        upper = (singleHeight + space) * i
        lower = upper + singleHeight
        box = map(int,[left, upper, right, lower])
        im.paste(singleImage, box)

print singleWidth, singleHeight

im.show()


#im.save("6pack.jpeg")
