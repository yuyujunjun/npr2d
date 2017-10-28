from PIL import Image
import random
import sys
secret = sys.argv[1]
dest=sys.argv[2]
resul=sys.argv[3]
im=Image.open(dest)
#get texture pic
atexture=Image.open(secret)
ar,ag,ab,aa=atexture.split()
atexture=aa
ablocksize=80


#get picture layer
r,g,b=im.split()
#make style picture laystyle.show()ers

#make style image
style=Image.merge('RGB',(r,g,b))
sr,sg,sb=style.split()
for i in range(style.height):
    for j in range(style.width):
         sr.putpixel((j,i),255)
         sg.putpixel((j,i),255)
         sb.putpixel((j,i),255)
#make brush size


#get block pixel quantization
def get_average(blockarray):
    sum=0
    for i in blockarray:
        sum=sum+i
    #return sum/len(blockarray)
    return blockarray[int(len(blockarray)/2)]
#get block pixel array
def get_array(block):
    blockarray=[]
    for i in range(blocksize):
        for j in range(blocksize):
            blockarray.append(block.getpixel((j,i)))
    return blockarray
#get single layer style color
def matchlayer(blockcolor,blocksize,TextureArray):
    blockCurColor=[]
    for i in range(blocksize):
        for j in range(blocksize):
            
            if (TextureArray[j*blocksize+i]<=0.7):
                blockCurColor.append(255)
            else :
                blockCurColor.append(int(TextureArray[j*blocksize+i]*blockcolor))
    return blockCurColor
#get three layer style color
def matchcolor(blockr,blockg,blockb,blocksize,TextureArray):
    blockarrayr=get_array(blockr)
    blockarrayg=get_array(blockg)
    blockarrayb=get_array(blockb)
    blockcolr=get_average(blockarrayr)
    blockcolg=get_average(blockarrayg)
    blockcolb=get_average(blockarrayb)
    BstyleR=matchlayer(blockcolr,blocksize,TextureArray)
    BstyleG=matchlayer(blockcolg,blocksize,TextureArray)
    BstyleB=matchlayer(blockcolb,blocksize,TextureArray)
    return [BstyleR,BstyleG,BstyleB]
#add block to style image
def moveCol2result(Bstyle,posi,posj,blocksize):
    for i in range(posi,posi+blocksize):
        for j in range(posj,posj+blocksize):
            ki=i-posi
            kj=j-posj
            if(sr.getpixel((j,i))>=250):
                sr.putpixel((j,i),Bstyle[0][kj*blocksize+ki])
            elif(Bstyle[0][kj*blocksize+ki]<230):
                sr.putpixel((j,i),int(0.6*Bstyle[0][kj*blocksize+ki]+0.4*sr.getpixel((j,i))))
            if(sg.getpixel((j,i))>=250):
                sg.putpixel((j,i),Bstyle[1][kj*blocksize+ki])
            elif(Bstyle[1][kj*blocksize+ki]<230):
                sg.putpixel((j,i),int(0.6*Bstyle[1][kj*blocksize+ki]+0.4*sg.getpixel((j,i))))
            if(sb.getpixel((j,i))>=250):
                sb.putpixel((j,i),Bstyle[2][kj*blocksize+ki])
            elif(Bstyle[2][kj*blocksize+ki]<230):
                sb.putpixel((j,i),int(0.6*Bstyle[2][kj*blocksize+ki]+0.4*sb.getpixel((j,i))))

i=int(ablocksize)
j=int(ablocksize)
while(True):
    blocksize=int(random.uniform(0.2*ablocksize,ablocksize))
    texture=atexture.rotate(int(random.uniform(0,180)));
    texture=texture.resize((blocksize,blocksize))
   
    #get texture layer
    #tr,tg,tb,ta=texture.split()
    ta=texture
    
    #get texture detail array
    TextureArray=[]
    for ii in range(blocksize):
        for jj in range(blocksize):
            TextureArray.append(ta.getpixel((jj,ii))/255)
            

    if(j+blocksize>style.width):
        i=int(i+0.1*blocksize+random.uniform(0,0.4*blocksize))
        j=int(random.uniform(0,0.3*blocksize))
    if(i+blocksize>style.height-blocksize):
        break
    tempi=i
    i=int(i+random.uniform(-0.5*blocksize,0.5*blocksize))#这是世界上最坑爹的函数，没有之一
    if(i<0):
        i=int(random.uniform(0,0.5*blocksize))

    blockr=r.crop((j,i,j+blocksize,i+blocksize))
    blockg=g.crop((j,i,j+blocksize,i+blocksize))
    blockb=b.crop((j,i,j+blocksize,i+blocksize))
    Bstyle=matchcolor(blockr,blockg,blockb,blocksize,TextureArray)
    
    moveCol2result(Bstyle,i,j,blocksize)
    j=int(j+random.uniform(0.1*blocksize,0.5*blocksize))
    i=tempi
style=Image.merge('RGB',(sr,sg,sb))
style.show()
style.save(resul)
