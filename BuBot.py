#!/usr/bin/env python
import tweepy, time, sys, urllib2, random, math
import matplotlib.pyplot as plt
from keys import keys
import colortools as ct

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
                table[id] = list()
                table[id].append(row[1])
                setti=dict()
                table[id].append(setti)
            table[id][1][row[0]]=1
    return table

def readReadymades(readymades, cMap):
    table={}
    lines=list()
    with open(readymades) as f:
    #skip headers
        line = next(f).rstrip().split("\t")
        for line in f:
            lines.append(line.rstrip().split("\t"))
        for i in cMap.keys():
            for row in lines:
                if row[0] in cMap[i][1].keys():
                    cMap[i][1][row[0]]+=1
                    if (row[0]+" "+row[1]) not in cMap[i][1].keys():   
                        cMap[i][1][row[0]+" "+row[1]]=1
                    else:  cMap[i][1][row[0]+" "+row[1]]+=1
                elif row[1] in cMap[i][1].keys():
                    cMap[i][1][row[1]]+=1
                    if (row[0]+" "+row[1]) not in cMap[i][1].keys():
                        cMap[i][1][row[0]+" "+row[1]]=1
                    else:  cMap[i][1][row[0]+" "+row[1]]+=1
    return cMap

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
    
#Plots a color
def showColor(color1, color2):
    fig = plt.figure(1, facecolor=color1.keys()[0])
    fig.canvas.set_window_title(color1.values()[0].copy().pop())
    ax = fig.add_subplot(1,1,1, axisbg=color2.keys()[0], label='everybot color')
    plt.show()
    
def initData():
    cMap=readColorMap("Veale's color map.csv", 2)
    rMs=readReadymades("Veale's bracketed color bigrams.csv", cMap)
    rMs=readReadymades("Veale's unbracketed color bigrams.csv", cMap)
    for i in cMap.keys():
        for j in cMap[i][1].keys():
            if cMap[i][1][j]==1 and len(cMap[i][1].keys())>2:
                del cMap[i][1][j]
    return cMap

if __name__ == "__main__":
    cMap=initData()
    #The following retrieves the color of everycolorbots last tweet
    with open("everycolorbot tweets.csv") as f:
    #skip headers
        line = next(f).rstrip().split("\t")
        for line in f:
            color='#'+line.rstrip().split("\t")[0][2:]
            [a,b,c,d,e,f]=ct.getBlendOfColors(color,cMap)
            if e<1 and f<100: #e is the color difference <1 is unrecognizable.
                showColor(ct.blendColors(a,b,c, d, cMap), {color:'test'})
##    api=login()
##    latest=api.user_timeline(id="everycolorbot", count=10)
##    lastTweet=[]
##    for status in latest:
##        lastTweet=status.text.split(' ')
##        #Change rgb representation
##        lastTweet[0]='#'+lastTweet[0][2:]
##        [a,b,c,d, e]=ct.getBlendOfColors(lastTweet[0], cMap)
##        if e<1: #e is the color difference <1 is unrecognizable.
##            showColor(ct.blendColors(a,b,c, d, cMap), {lastTweet[0]:'test'})
        
        #Test with rgb and euc-distance
##        closestDist=getColorDistance(RGB2List(closestColor.keys()[0]), RGB2List(lastTweet[0]))
##        for key in vealesColorMap.keys():
##            dist=getColorDistance(RGB2List(key), RGB2List(lastTweet[0]))
##            if dist<closestDist:
##                closestDist=dist
##                closestColor={key:vealesColorMap[key]}
##
##        closestDist=getUVDistance(RGB2YUV(closestColor.keys()[0]), RGB2YUV(lastTweet[0]))
##        for key in vealesColorMap.keys():
##            dist=getUVDistance(RGB2YUV(key), RGB2YUV(lastTweet[0]))
##            if dist<closestDist:
##                closestDist=dist
##                closestColor={key:vealesColorMap[key]}
##        #print closestColor
##        #print getColorDistance(RGB2List(closestColor.keys()[0]), RGB2List(lastTweet[0]))
##        #print getCompDist(RGB2YUV(closestColor.keys()[0]), RGB2YUV(lastTweet[0]))
##        #print getUVDistance(RGB2YUV(closestColor.keys()[0]), RGB2YUV(lastTweet[0]))
##        
##        
##        #Show closest color to everybots latest tweet
##        
##        #Match luma to ecb-color, store correction amount.
##        matchedY, correction=matchY(lastTweet[0],closestColor.keys()[0])
##        #print correction
##        #If the correction wasn't too drastic and the color was close enough, show color.
##        if math.sqrt(correction**2)<20 and getUVDistance(RGB2YUV(closestColor.keys()[0]), RGB2YUV(lastTweet[0]))<15:
##            showColor({matchedY:closestColor.values()[0]}, {lastTweet[0]:set(lastTweet[1])})
##
##        
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