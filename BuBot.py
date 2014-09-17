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

#Cast rgb hex code to int list.
def RGB2List(rgb):
    if len(rgb)==7:
        return (int(rgb[1:3],16),int(rgb[3:5],16),int(rgb[5:7],16))
    else: return 0

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
def showColor(color):
    fig = plt.figure(1, facecolor=color.keys()[0])
    fig.canvas.set_window_title(color.values()[0].pop())
    plt.show()
    
def initData():
    vealesColorMap=readColorMap("Veale's color map.csv", 2)
    
    return [vealesColorMap]
if __name__ == "__main__":
    vealesColorMap=initData()[0]
    #The following retrieves the color of everycolorbots last tweet
    api=login()
    latest=api.user_timeline(id="everycolorbot", count=10)
    lastTweet=[]
    for status in latest:
        lastTweet=status.text.split(' ')
        #Change rgb representation
        lastTweet[0]='#'+lastTweet[0][2:]
        print lastTweet
        closestColor={"#000000": set(['death black', 'pitch black'])}
        closestDist=getColorDistance(RGB2List(closestColor.keys()[0]), RGB2List(lastTweet[0]))
        for key in vealesColorMap.keys():
            dist=getColorDistance(RGB2List(key), RGB2List(lastTweet[0]))
            if dist<closestDist:
                closestDist=dist
                closestColor={key:vealesColorMap[key]}
        print closestColor
        print getColorDistance(RGB2List(closestColor.keys()[0]), RGB2List(lastTweet[0]))
        #Show closest color to everybots latest tweet
        showColor(closestColor)
        #Show everycolorbots last tweets color
        showColor({lastTweet[0]:set(lastTweet[1])})
        
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