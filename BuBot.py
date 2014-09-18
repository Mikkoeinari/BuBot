#!/usr/bin/env python
import tweepy, time, sys, urllib2, random, math
import matplotlib.pyplot as plt
from keys import keys

def login():
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

#Reads color map into memory, idcol is the column that stores the rgb code
def readColorMap(filename, idcol):
    table={}
    with open(filename) as f:
        #skip headers
        line = next(f).rstrip().split("\t")
        for line in f:
            row = line.rstrip().split("\t")
            #Skip the bad record in input
            if len(row)<idcol+1:
                continue
            #Add the rows to table, there are multiple rows with same key(rgb code)
            id=row[idcol]
            if not id in table:
                table[id] = set()
            table[id].add(row[0]+" "+row[1])
    return table

#euclidian distance between two points in rgb space
def getColorDistance(first, second):
    return(math.sqrt((first[0]-second[0])**2+(first[1]-second[1])**2+(first[2]-second[2])**2))


#Distances of individual RGB components from another RGB color
def getCompDist(first, second):
    return[(first[0]-second[0]),(first[1]-second[1]),(first[2]-second[2])]
    
#Euclidian distance betveen YUV colorspaces U and V values
def getUVDistance(first, second):
    return(math.sqrt((first[1]-second[1])**2+(first[2]-second[2])**2))

#YUV conversion  from rgb colorspace from wikipedia
def RGB2YUV(rgb):
    Wr=0.299
    Wg=0.587
    Wb=0.114
    Umax=0.436
    Vmax=0.615
    if len(rgb)==7:
        R=int(rgb[1:3],16)
        G=int(rgb[3:5],16)
        B=int(rgb[5:7],16)
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
    return List2RGB([R,G,B])

#Cast rgb hex code to int list.
def RGB2List(rgb):
    if len(rgb)==7:
        return (int(rgb[1:3],16),int(rgb[3:5],16),int(rgb[5:7],16))
    else: return (0,0,0)
    
#Cast a list of rgb values to hex code
def List2RGB(rgblist):
    if len(rgblist)==3:
        return '#'+format(rgblist[0],'x')+format(rgblist[1],'x')+format(rgblist[2],'x')
    else: return "#000000"


#search function
def readTweets(api, query):
    #read all tweets that satisfy serch conditions
    return api.search(query, lang='en')
#update status
def updateStatus(api, status):
    api.update_status(status)
#send private messages
def sendPrivate(api, message, user):
    api.update_status(user+" "+message)

#Retrieve content from internet
#Not needed atm
def getText():
    response = urllib2.urlopen('http://python.org/')
    html = response.read()
    
#Match the luma of the two colors
def matchY(first, second):
    source=RGB2YUV(first)
    target=RGB2YUV(second)
    correction=target[0]-source[0]
    target[0]=source[0]
    return [YUV2RGB(target), correction]

#Plots a color
def showColor(color1, color2):
    fig = plt.figure(1, facecolor=color1.keys()[0])
    fig.canvas.set_window_title(color1.values()[0].pop())
    ax = fig.add_subplot(1,1,1, axisbg=color2.keys()[0], label='everybot color')
    plt.show()
    
def initData():
    vealesColorMap=readColorMap("Veale's color map.csv", 2)
    return [vealesColorMap]

def blendColors(first,second, ratio):
    yuv1=RGB2YUV(first[0])
    yuv2=RGB2YUV(second[0])
    resultName=first[1].pop().split(' ')[0]+' '+second[1].pop().split(' ')[0]
    resultColor=YUV2RGB([(yuv1[0]*ratio+yuv2[0]*(1-ratio))/2, (yuv1[1]*ratio+yuv2[1]*(1-ratio))/2,(yuv1[2]*ratio+yuv2[2]*(1-ratio))/2])
    return {resultColor:set([resultName])}

if __name__ == "__main__":
    vealesColorMap=initData()[0]
    print vealesColorMap.items()[0]
    showColor(blendColors(vealesColorMap.items()[0],vealesColorMap.items()[10], 0.8), {vealesColorMap.items()[10][0]:vealesColorMap.items()[0][1].pop()})
    #The following retrieves the color of everycolorbots last tweet
    api=login()
    latest=api.user_timeline(id="everycolorbot", count=10)
    lastTweet=[]
    for status in latest:
        lastTweet=status.text.split(' ')
        #Change rgb representation
        lastTweet[0]='#'+lastTweet[0][2:]
        #print lastTweet
        closestColor={"#000000": set(['pitch black'])}
        
        #Test with rgb and euc-distance
##        closestDist=getColorDistance(RGB2List(closestColor.keys()[0]), RGB2List(lastTweet[0]))
##        for key in vealesColorMap.keys():
##            dist=getColorDistance(RGB2List(key), RGB2List(lastTweet[0]))
##            if dist<closestDist:
##                closestDist=dist
##                closestColor={key:vealesColorMap[key]}

        closestDist=getUVDistance(RGB2YUV(closestColor.keys()[0]), RGB2YUV(lastTweet[0]))
        for key in vealesColorMap.keys():
            dist=getUVDistance(RGB2YUV(key), RGB2YUV(lastTweet[0]))
            if dist<closestDist:
                closestDist=dist
                closestColor={key:vealesColorMap[key]}
##        #print closestColor
##        #print getColorDistance(RGB2List(closestColor.keys()[0]), RGB2List(lastTweet[0]))
##        #print getCompDist(RGB2YUV(closestColor.keys()[0]), RGB2YUV(lastTweet[0]))
##        #print getUVDistance(RGB2YUV(closestColor.keys()[0]), RGB2YUV(lastTweet[0]))
        
        
        #Show closest color to everybots latest tweet
        
        #Match luma to ecb-color, store correction amount.
        matchedY, correction=matchY(lastTweet[0],closestColor.keys()[0])
        #print correction
        #If the correction wasn't too drastic and the color was close enough, show color.
        if math.sqrt(correction**2)<20 and getUVDistance(RGB2YUV(closestColor.keys()[0]), RGB2YUV(lastTweet[0]))<15:
            showColor({matchedY:closestColor.values()[0]}, {lastTweet[0]:set(lastTweet[1])})

        
#Test code, all functional but obsolete
##    api=login()
##    i=1
##    while i==1:
##        r=random.random()
##        if r<0.5:
##            statuses=readTweets(api, '"my mom"')
##        else:
##            statuses=readTweets(api, '"my dog"')
##        #getText()
##        if statuses:
##            for status in statuses:
##                if "RT" and "@" not in status.text:
##                    if "http" not in status.text:
##                        if len(status.text)<120:
##                            if r<0.5:
##                                text=status.text.encode('ascii', 'replace').split("#")[0]
##                                text=text.lower().replace("dad", "shaver")
##                                print text.replace("my mom", "my twitterbot")
##                                #updateStatus(api, text.replace("my mom", "my twitterbot"))
##                            else:
##                                text=status.text.encode('ascii', 'replace').split("#")[0]
##                                print text.lower().replace("my dog", "my twitterbot")
##                                #updateStatus(api, text.lower().replace("my dog", "my bot"))
##                            break;
##        for k in range(10):
##            time.sleep(3)
##            print 'tic %i' % k
##    