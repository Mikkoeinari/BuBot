#!/usr/bin/env python
import tweepy, time, sys, urllib2, random, math
import matplotlib.pyplot as plt
from keys import keys
import colortools as ct
from copy import deepcopy
import atexit, pickle, sys, signal




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
        #Pointer madness alert!!!
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
def updateStatus(api, status, id=None):
    api.update_status(status, id)
    
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
    oMap=deepcopy(cMap)
    cMap=readReadymades("Veale's bracketed color bigrams.csv", cMap)
    cMap=readReadymades("Veale's unbracketed color bigrams.csv", cMap)
    for i in cMap.keys():
        for j in cMap[i][1].keys():
            if cMap[i][1][j]==1 and len(cMap[i][1].keys())>2:
                del cMap[i][1][j]
    return cMap, oMap

def getOrigName(color, map):
    return map[color][1].keys()[0]+" "+map[color][0]

#functions to save status of the system when extiting
def saveSystem(braglist, rtlist):
    pickle.dump(braglist, open("braggedTweets.txt", "wb"))
    pickle.dump(rtlist, open("reTweets.txt", "wb"))
def initBragged():
    try:
        return pickle.load(open("braggedTweets.txt", "r"))
    except(IOError):
        print "no tweets bragged, continuing..."
        return list()
def initRetweeted():
    try:
        return pickle.load(open("reTweets.txt", "r"))
    except(IOError):
        print "no retweets, continuing..."
        return list()
    

#main function
if __name__ == "__main__":
    
    [cMap, oMap]=initData()
    bragged=initBragged()
    retweeted=initRetweeted()
    api=login()
    #signal handler
    def signal_term_handler(signal, frame):
        print 'Exiting...'
        saveSystem(bragged, retweeted)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    while 1==1:
        #Try to get the last tweet, name the color and send the color name as a private message.
        try:
            #get my statuses and see if i have favorited tweets
            myTweets=api.user_timeline(count=100)
            for status in myTweets:
                #if my status is favorited more than once
                if status.favorite_count>1 and status.id not in bragged:
                    #Get the original tweet and the retweeted colour name from tweet.
                    name=status.text.split("called ")[1].split(".")[0]
                    ECBTweet=status.text.split("everycolorbot ")[1]
                    #Compose a bragging message
                    message="@everycolorbot I named your colour "+ECBTweet+" "+name+", and they like it!"
                    print message
                    #Update the list of bragged retweets
                    bragged.append(status.id)
                    #send private message to ECB
                    updateStatus(api, message)
                    #if successful save the system
                    saveSystem(bragged, retweeted)
                    
            #Read latest tweet from ECB and see if that can be named
            latest=api.user_timeline(id="everycolorbot", count=1)
            lastTweet=[]
            #for loop is not necessary anymore, i used it when i did test with more tweets.
            for status in latest:
                #break if 
                if status.id in retweeted: break
                lastTweet=status.text.split(' ')
                #Change rgb representation 0x to #
                lastTweet[0]='#'+lastTweet[0][2:]
                
                #Get the color mix
                [color1,color2,ratio,blendedColor,colorDistance,componentDistance]=ct.getBlendOfColors(lastTweet[0],cMap)
                
                #wellness function, if color difference is too great or the distance of the blending colors
                #or the blending ratio is too small skip the tweet
                if colorDistance<2 and componentDistance<100 and ratio>0.2 and ratio<0.8:
                        #get the color name
                        #white or black is never the defining color under these conditions, change that to the head.
                        if oMap[color2][0]=='white' or oMap[color2][0]=='black':
                            suggestion=ct.blendColors(color2,color1,ratio, blendedColor, cMap).values()[0].pop()
                        else:   suggestion=ct.blendColors(color1,color2,ratio, blendedColor, cMap).values()[0].pop()
                        originals= getOrigName(color1, oMap)+" and " +getOrigName(color2,oMap)
                        #message="@everycolorbot "+"I think the color looks a bit like "+suggestion+ ". A mix of "+originals+"."
                        message="This color is called "+suggestion+". RT: "+"@everycolorbot "+status.text
                        print ratio
                        print message
                        #save the status id into retweeted list
                        retweeted.append(status.id)
                        #comment the next line if you don't want to stop the bot from sending replys to ecb
                        updateStatus(api, message)
                        #if successful, save the system
                        saveSystem(bragged, retweeted)
                        #uncomment the next line for sanitycheck
                        ##showColor(ct.blendColors(color1,color2,ratio, blendedColor, cMap), {lastTweet[0]:'tweet'})
                        
                else: 
                    print "wellness not good :("

                        
        #in case of error, wait a minute and retry.
        except tweepy.error.TweepError as error: 
            print error
            print "error, trying again in 5 minutes"
            time.sleep(300)
            continue
        
        #If succesful, wait for an hour+100 s. to avoid retweeting the same color twice.
        print "Napping..."
        time.sleep(3700)
    atexit.register(saveBragged, braglist=bragged, rtlist=retweeted)
    

 
    