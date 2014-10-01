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

#reads the readymades and organizes them to a data structure. 
#a lot of pointer code but essentially i just split the readymades into components and 
#store them into relevant lists.
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
def sendPrivate(api, user, message):
    api.send_direct_message(user=user, text=message)

#Retrieve content from internet
#Not needed atm
def getText():
    response = urllib2.urlopen('http://python.org/')
    html = response.read()
    
#Plots a color used for sanity checking the colorblending
def showColor(color1, color2):
    fig = plt.figure(1, facecolor=color1.keys()[0])
    fig.canvas.set_window_title(color1.values()[0].copy().pop())
    ax = fig.add_subplot(1,1,1, axisbg=color2.keys()[0], label='everybot color')
    plt.show()
    
#initializes the data structure for the color names
def initData():
    cMap=readColorMap("Veale's color map.csv", 2)
    rMs=readReadymades("Veale's bracketed color bigrams.csv", cMap)
    rMs=readReadymades("Veale's unbracketed color bigrams.csv", cMap)
    for i in cMap.keys():
        for j in cMap[i][1].keys():
            if cMap[i][1][j]==1 and len(cMap[i][1].keys())>2:
                del cMap[i][1][j]
    return cMap

#main function
if __name__ == "__main__":
    
    cMap=initData()
    api=login()
    
    while 1==1:
        #Try to get the last tweet, name the color and send the color name as a private message.
        try:
            latest=api.user_timeline(id="everycolorbot", count=1)
            lastTweet=[]
            for status in latest:
                lastTweet=status.text.split(' ')
                
                #Change rgb representation 0x to #
                lastTweet[0]='#'+lastTweet[0][2:]
                
                #Get the color mix
                [color1,color2,ratio,blendedColor,colorDistance,componentDistance]=ct.getBlendOfColors(lastTweet[0],cMap)
                
                #wellness function, if color difference is too great or the distance of the blending colors
                #or the blending ratio is too small skip the tweet
                if colorDistance<2 and componentDistance<100:
                    if ratio>0.2:
                        #get the color name
                        suggestion=ct.blendColors(color1,color2,ratio, blendedColor, cMap).values()[0].pop()
                        print "Regarding your last tweet. I think the color looks a bit like "+ suggestion
                        #comment the next line if you don't want to stop the bot from sending replys to ecb
                        updateStatus(api, "@everycolorbot "+"Regarding your last tweet. I think the color looks a bit like "+ suggestion)
                        #uncomment the next line for sanitycheck
                        #showColor(ct.blendColors(color1,color2,ratio, blendedColor, cMap), {lastTweet[0]:'tweet'})
                        
        #in case of error, wait a minute and retry.
        except tweepy.error.TweepError as error: 
            print error
            print "error, trying again in 5 minutes"
            time.sleep(300)
            continue
        
        #If succesful, wait for an hour and a half
        for k in range(90):
            time.sleep(60)
            print 'tic %i' % k
