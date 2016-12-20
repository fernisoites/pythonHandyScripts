from PIL import Image
from PIL import ImageDraw, ImageFont
import textwrap

def drawRectangle(it,color):
    draw.rectangle([it.left,it.up,it.right,it.down],fill=color,outline=color)

def drawDottedLine(end1,end2,space):
    x0, y0=end1
    x1, y1=end2
    num=int((y1-y0)*1.0/space)
    xSpace=(x1-x0)*1.0/num
    outList=[]
    
    for i in range(num):
        x=x0+i*xSpace
        y=y0+i*space
        outList+=[x,y]
    return outList

def drawTriangle(it,color):
    draw.polygon([it.point1[0],it.point1[1],
                  it.point2[0],it.point2[1],
                  it.point3[0],it.point3[1]],
                 outline=color,fill=color)
    return

class triangle():
    def __init__(self,point1,point2,point3):
        self.point1=point1
        self.point2=point2
        self.point3=point3

    def locate(self,left,up):
        self.up=up
        self.left=left


    
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

class line():
    def __init__(self,end1,end2):
        self.end1=end1
        self.end2=end2
        

pic=rectangle(1025,512)

im=Image.new("RGB",(pic.width,pic.height), "white")

# Define all rectangle objects:
gene=rectangle(pic.width*7/8,pic.height/30)
gene.locate(pic.width/16,pic.height/10)

exon2=rectangle(gene.width/6,pic.height/20)
exon2.locate(pic.width*2/5,gene.up-(exon2.height-gene.height)/2)

exon3=rectangle(gene.width/8,pic.height/20)
exon3.locate(exon2.left+gene.width*2/7,exon2.up)

intron2=rectangle(exon2.width/4,gene.height/2)
intron2.locate(exon2.left-exon2.width/2,gene.up/4)

intron3=rectangle(exon2.width/4,intron2.height)
intron3.locate(exon2.right+exon2.width/4, gene.up/4)

f1=rectangle(intron2.width,intron2.height)
f1.locate(intron2.left-intron2.width*3/2,gene.up*3)

f2=rectangle(intron2.width,intron2.height)
f2.locate(intron2.left+intron2.width*3/2,gene.up*3)

f3=rectangle(intron2.width,intron2.height)
f3.locate(intron3.left-intron2.width*3/2,gene.up*3)

f4=rectangle(intron2.width,intron2.height)
f4.locate(intron3.left+intron2.width*3/2,gene.up*3)

#Define space between dots in dotted lines.
space=exon2.height*1.0/5

#Define exon text
font = ImageFont.truetype("arial.ttf", 19)
e2Txtup=exon2.up+exon2.height/8
e2TxtLeft=exon2.left+exon2.width*2/7
e3Txtup=exon3.up+exon3.height/8
e3TxtLeft=exon3.left+exon2.width/7

#Begin drawing
draw=ImageDraw.Draw(im)

#draw gene, exon, txt
drawRectangle(gene,"BLACK")
drawRectangle(exon2,"#62A9E3")
drawRectangle(exon3,"#62A9E3")

draw.text([e2TxtLeft,e2Txtup],"Exon2",fill="BLACK",font=font)
draw.text([e3TxtLeft,e3Txtup],"Exon3",fill="BLACK",font=font)

#replicate gene and exons
region=im.crop((0,0,pic.width,pic.height/4))
im.paste(region,(0,pic.height*3/4,pic.width,pic.height))

#Draw introns on top.
drawRectangle(intron2,"BLACK")
drawRectangle(intron3,"BLACK")

#Draw dotted lines.
line1=line([intron2.left,intron2.down],[intron2.left+exon2.width/8,gene.down])
line1Axis=drawDottedLine(line1.end1,line1.end2,space)
draw.point(line1Axis,fill="BLACK")
line2=line([intron2.right,intron2.down],[intron2.left+exon2.width/8,gene.down])
line2Axis=drawDottedLine(line2.end1,line2.end2,space)
draw.point(line2Axis,fill="BLACK")
line3=line([intron3.left,intron3.down],[intron3.left+exon2.width/8,gene.down])
line3Axis=drawDottedLine(line3.end1,line3.end2,space)
draw.point(line3Axis,fill="BLACK")
line4=line([intron3.right,intron3.down],[intron3.left+exon2.width/8,gene.down])
line4Axis=drawDottedLine(line4.end1,line4.end2,space)
draw.point(line4Axis,fill="BLACK")

#Draw introns below
drawRectangle(f1,"BLACK")
drawRectangle(f2,"BLACK")
drawRectangle(f3,"BLACK")
drawRectangle(f4,"BLACK")

#Draw more dotted lines.
line5=line([intron2.left+exon2.width/8-intron2.width,gene.up],[f1.left,f1.down])
line5Axis=drawDottedLine(line5.end1,line5.end2,space)
draw.point(line5Axis,fill="BLACK")
line6=line([intron2.left+exon2.width/8,gene.up],[f1.right,f1.down])
line6Axis=drawDottedLine(line6.end1,line6.end2,space)
draw.point(line6Axis,fill="BLACK")
line7=line(line6.end1,[f2.left,f2.down])
line7Axis=drawDottedLine(line7.end1,line7.end2,space)
draw.point(line7Axis,fill="BLACK")
line8=line([intron2.left+exon2.width/8+intron2.width,gene.up],[f2.right,f2.down])
line8Axis=drawDottedLine(line8.end1,line8.end2,space)
draw.point(line8Axis,fill="BLACK")

line9=line([intron3.left+exon2.width/8-intron2.width,gene.up],f3.ld)
line9Axis=drawDottedLine(line9.end1,line9.end2,space)
draw.point(line9Axis,fill="BLACK")
line10=line([intron3.left+exon2.width/8,gene.up],f3.rd)
line10Axis=drawDottedLine(line10.end1,line10.end2,space)
draw.point(line10Axis,fill="BLACK")
line11=line(line10.end1,f4.ld)
line11Axis=drawDottedLine(line11.end1,line11.end2,space)
draw.point(line11Axis,fill="BLACK")
line12=line([intron3.left+exon2.width/8+intron3.width,gene.up],f4.rd)
line12Axis=drawDottedLine(line12.end1,line12.end2,space)
draw.point(line12Axis,fill="BLACK")


#Define enzyme
enzymeHeight=f1.height/3
enzymeWidth=(f2.left-f1.right)*2/3

#Draw enzymes
enzyme1=rectangle(enzymeWidth, enzymeHeight)
enzyme1.locate(f1.right,(f1.up+f1.down)/2)
drawRectangle(enzyme1,"GREEN")

enzyme2=rectangle(enzymeWidth, enzymeHeight)
enzyme2.locate(f3.right,(f1.up+f1.down)/2)
drawRectangle(enzyme2,"GREEN")

#Draw Loxp shapes
triangle1=triangle([f1.right+(f2.left-f1.right)*2/3,f1.up],
                   [f1.right+(f2.left-f1.right)*2/3,f1.down],
                   [f2.left,(f1.up+f1.down)/2])

triangle2=triangle([f3.right+(f2.left-f1.right)*2/3,f3.up],
                   [f3.right+(f2.left-f1.right)*2/3,f3.down],
                   [f4.left,(f1.up+f1.down)/2])

drawTriangle(triangle1,"RED")
drawTriangle(triangle2,"RED")

#Draw large arrow
arrowBody=rectangle(gene.height,exon3.width)
arrowBody.locate((exon2.left+exon2.right)/2,f2.down+f2.height*8)
drawRectangle(arrowBody,"BLACK")

arrowHead=triangle([arrowBody.left-arrowBody.width,arrowBody.down],
                   [arrowBody.right+arrowBody.width,arrowBody.down],
                   [(arrowBody.left+arrowBody.right)/2,arrowBody.down+arrowBody.width*2])
                   
drawTriangle(arrowHead,"BLACK")

#Draw more text
f1TxtLeft=f1.left-f1.width*4
f1TxtUp=f1.up-f1.height
f2TxtLeft=f4.right+f4.width/2
f2TxtUp=f1.up-f1.height

draw.text([f1TxtLeft,f1TxtUp],"Oligo Donor 1",fill="BLACK",font=font)
draw.text([f2TxtLeft,f2TxtUp],"Oligo Donor 2",fill="BLACK",font=font)


res1TxtLeft=f1.left
res1TxtUp=f1.down+f1.height
enz1TxtLeft=f1.left
enz1TxtUp=res1TxtUp+f1.height*2
lox1TxtLeft=enzyme1.right
lox1TxtUp=f1.down+f1.height

font1 = ImageFont.truetype("arial.ttf", 16)
draw.text([res1TxtLeft,res1TxtUp],"Restriction",fill="GREEN",font=font1)
draw.text([enz1TxtLeft,enz1TxtUp],"Enzyme 1",fill="GREEN",font=font1)
draw.text([lox1TxtLeft,lox1TxtUp],"Loxp",fill="RED",font=font)

res2TxtLeft=f3.left
res2TxtUp=f3.down+f3.height
enz2TxtLeft=f3.left
enz2TxtUp=res2TxtUp+f3.height*2
lox2TxtLeft=enzyme2.right
lox2TxtUp=f3.down+f3.height

draw.text([res2TxtLeft,res2TxtUp],"Restriction",fill="GREEN",font=font1)
draw.text([enz2TxtLeft,enz2TxtUp],"Enzyme 2",fill="GREEN",font=font1)
draw.text([lox2TxtLeft,lox2TxtUp],"Loxp",fill="RED",font=font)


text="Inject PX458-C1q-I2, PX458-C1q-I3, donor 1, donor 2 into podocyte cell line"
lines=textwrap.wrap(text,width=20)

y_text =arrowBody.up
font2 = ImageFont.truetype("arial.ttf", 30)

for line in lines:
    width, height =font.getsize(line)
    draw.text((arrowBody.right+arrowBody.width*3,y_text),line,font=font2,fill="BLACK")
    y_text+=height*3/2

del draw


im.save("c1q.jpeg")
