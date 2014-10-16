#!/usr/bin/env python
import math, operator, random

#Point class
class Point:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        self.xyz=[x,y,z]

#Finds the closest point of P on a line A,B
def GetClosestPoint(A, B, P):
    a_to_p = [P.x - A.x, P.y - A.y, P.z - A.z]     # Storing vector A->P
    a_to_b = [B.x - A.x, B.y - A.y, B.z - A.z]     # Storing vector A->B
    atb2 = a_to_b[0]**2 + a_to_b[1]**2 + a_to_b[2]**2
    atp_dot_atb = a_to_p[0]*a_to_b[0] + a_to_p[1]*a_to_b[1]+a_to_p[2]*a_to_b[2]
    if atb2==0:
        return Point(0,0,0)
    t = atp_dot_atb / atb2 
    if t>1 or t<0:
        return Point(0,0,0)
    return Point(A.x + a_to_b[0]*t ,A.y + a_to_b[1]*t, A.z + a_to_b[2]*t)

#euclidian distance between two points in 3d color space
def getColorDistance(first, second):
    return(math.sqrt((first[0]-second[0])**2+(first[1]-second[1])**2+(first[2]-second[2])**2))

#Distances of individual RGB components from another RGB color
def getCompDist(first, second):
    return[(first[0]-second[0]),(first[1]-second[1]),(first[2]-second[2])]
    
#Euclidian distance betveen YUV colorspaces U and V values
def getUVDistance(first, second):
    return(math.sqrt((first[1]-second[1])**2+(first[2]-second[2])**2))
#Distance of two points in 3d, (same as color distance, but with Points)
def getPointDistance(A,B):
    return(math.sqrt((A.x-B.x)**2+(A.y-B.y)**2+(A.z-B.z)**2))
#rgb to xyz conversion
#formulas from http://www.easyrgb.com/index.php?X=MATH
def RGB2XYZ(rgb):
    rgb=RGB2List(rgb)
    var_R = ( rgb[0] / float(255) )        
    var_G = ( rgb[1] / float(255) )        
    var_B = ( rgb[2] / float(255) )
    if ( var_R > 0.04045 ): var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_R = var_R / 12.92
    if ( var_G > 0.04045 ): var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_G = var_G  / 12.92
    if ( var_B > 0.04045 ): var_B = ( ( var_B  + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_B = var_B  / 12.92
    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
    return [X,Y,Z]

def XYZ2RGB(xyz):
    var_X = xyz[0] / 100        
    var_Y = xyz[1] / 100        
    var_Z = xyz[2] / 100 
    var_R = var_X *  3.2406 + var_Y * -1.5372 + var_Z * -0.4986
    var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415
    var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570
    if ( var_R > 0.0031308 ): var_R = 1.055 * ( var_R ** ( 1 / 2.4 ) ) - 0.055
    else:                     var_R = 12.92 * var_R
    if ( var_G > 0.0031308 ): var_G = 1.055 * ( var_G ** ( 1 / 2.4 ) ) - 0.055
    else:                     var_G = 12.92 * var_G
    if ( var_B > 0.0031308 ): var_B = 1.055 * ( var_B ** ( 1 / 2.4 ) ) - 0.055
    else:                     var_B = 12.92 * var_B
    R =int( var_R * 255)
    G =int( var_G * 255)
    B =int( var_B * 255)
    return List2RGB([R,G,B])
    
def XYZ2CIE(xyz):
    var_X = xyz[0]/float(95.047)
    var_Y = xyz[1]/float(100.000)
    var_Z = xyz[2]/float(108.883)
    if ( var_X > 0.008856 ): var_X = var_X ** ( 1/3.0 )
    else:                    var_X = ( 7.787 * var_X ) + ( 16 / 116 )
    if ( var_Y > 0.008856 ): var_Y = var_Y ** ( 1/3.0 )
    else:                    var_Y = ( 7.787 * var_Y ) + ( 16 / 116 )
    if ( var_Z > 0.008856 ): var_Z = var_Z ** ( 1/3.0 )
    else:                    var_Z = ( 7.787 * var_Z ) + ( 16 / 116 )
    L = ( 116 * var_Y ) - 16
    a = 500 * ( var_X - var_Y )
    b = 200 * ( var_Y - var_Z )
    return [L,a,b]
    
def CIE2XYZ(cie):
    var_Y = ( cie[0] + 16 ) / 116
    var_X = cie[1] / 500 + var_Y
    var_Z = var_Y - cie[2] / 200
    if ( var_Y**3 > 0.008856 ): var_Y = var_Y**3
    else:                      var_Y = ( var_Y - 16 / 116 ) / 7.787
    if ( var_X**3 > 0.008856 ): var_X = var_X**3
    else:                      var_X = ( var_X - 16 / 116 ) / 7.787
    if ( var_Z**3 > 0.008856 ): var_Z = var_Z**3
    else:                      var_Z = ( var_Z - 16 / 116 ) / 7.787
    X = 95.047 * var_X   
    Y = 100.000 * var_Y  
    Z = 108.883 * var_Z     

    return [X,Y,Z]

def RGB2CIE(rgb):
    return XYZ2CIE(RGB2XYZ(rgb))
def CIE2RGB(cie):
    return XYZ2RGB(CIE2XYZ(cie))

#YUV conversion  from rgb colorspace from wikipedia
def RGB2YUV(rgb):
    Wr=0.299
    Wg=0.587
    Wb=0.114
    Umax=0.436
    Vmax=0.615

    if len(rgb)==7:
        [R,G,B]=RGB2List(rgb)
    elif len(rgb)==3:
        R=rgb[0]
        G=rgb[1]
        B=rgb[2]
    Y=R*Wr+G*Wg+B*Wb
    U=Umax*(B-Y)/(1-Wb)
    V=Vmax*(R-Y)/(1-Wr)
    return [Y,U,V]

#From YUV space to RGB space
def YUV2RGB(YUV):
    Wr=0.299
    Wg=0.587
    Wb=0.114
    Umax=0.436
    Vmax=0.615
    Y=YUV[0]
    U=YUV[1]
    V=YUV[2]
    R=int(Y+V*((1-Wr)/Vmax))
    G=int(Y-U*((Wb*(1-Wb))/(Umax*Wg))-V*((Wr*(1-Wr))/(Vmax*Wg)))
    B=int(Y+U*((1-Wb)/Umax))
    if R>255:
        R=255
    if G>255:
        G=255
    if B>255:
        B=255
    if R<0:
        R=0
    if G<0:
        G=0
    if B<0:
        B=0
    return List2RGB([R,G,B])

#Cast rgb hex code to int list.
def RGB2List(rgb):
    if len(rgb)==7:
        return (int(rgb[1:3],16),int(rgb[3:5],16),int(rgb[5:7],16))
    else: 
        return (0,0,0)
    
#Cast a list of rgb values to hex code
def List2RGB(rgblist):
    if len(rgblist)==3:
        R=format(int(rgblist[0]),'x')
        G=format(int(rgblist[1]),'x')
        B=format(int(rgblist[2]),'x')
        #Make this better
        if len(R)<2:
            R='0'+R
        if len(G)<2:
            G='0'+G
        if len(B)<2:
            B='0'+B
        return '#'+R+G+B 
    else: return "#000000"

#Match the luma of the two colors
def matchY(first, second):
    source=RGB2YUV(first)
    target=RGB2YUV(second)
    correction=target[0]-source[0]
    target[0]=source[0]
    return [YUV2RGB(target), correction]

def getRandom(lista):
    sortedLista = sorted(lista.items(), key=operator.itemgetter(1))
    listsum=sum(lista.values())
    item=sortedLista[0][0]
    if len(sortedLista)>1:
        i=random.randrange(listsum)
        j=0
        while i>0:
            item=sortedLista[j][0]
            i-=sortedLista[j][1]
            j+=1
    return item

def getBaseColor(lista):
    return lista[0]
    
def blendColors(first,second, ratio,rgb, cMap):
    a=getRandom(cMap[first][1])
    b=getRandom(cMap[second][1])
    d=getBaseColor(cMap[second])
    c=a+" "+b+" "+d
    resultName=c
    resultColor=rgb
    ci=RGB2CIE(first)
    cj=RGB2CIE(second)
    A=Point(ci[0],ci[1],ci[2])
    B=Point(cj[0],cj[1],cj[2])
    dist=getPointDistance(A,B)
    #print first, second, ratio, dist, resultColor,resultName
    return {resultColor:set([resultName])}
    

#Try to find the best color or colors to represent the arg
#measure dist from line color1-color2 to find closest match.
def getBlendOfColors(color, cMap):
    blend=('#FFFFFF')
    ratio=0.5
    luma=-1
    sample=RGB2CIE(color)
    bestDist=100000000
    for i in cMap.keys():
        for j in cMap.keys():
            ci=RGB2CIE(i)
            cj=RGB2CIE(j)
            A=Point(ci[0],ci[1],ci[2])
            B=Point(cj[0],cj[1],cj[2])
            P=Point(sample[0],sample[1],sample[2])
            AxB=GetClosestPoint(A,B,P)
            dist=getPointDistance(AxB,P)
            d1=getPointDistance(A, AxB)
            d2=getPointDistance(B, AxB)
            if dist<bestDist and dist>0 and (d2/(d1+d2)>0.2 or d2/(d1+d2)<0.8):
                bestDist=dist
                if d2/(d1+d2)>d1/(d1+d2):
                    color1=j
                    color2=i
                    ratio= d2/(d1+d2)
                else:
                    color1=i
                    color2=j
                    ratio= d1/(d1+d2)
                blend= CIE2RGB([AxB.x, AxB.y,AxB.z])
                #print color1, color2, ratio, dist
                abDist=getPointDistance(A,B)
    return [color1, color2, ratio, blend, bestDist, abDist]


