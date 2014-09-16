#!/usr/bin/env python
import tweepy, time, sys, urllib2, random
from keys import keys

def login():
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


#What could i do here? Take corpus from twitter? Have a searate corpus as db
#Deep blue
#shallowblue
#rabbit in rapid rabid
def readTable(filename, prefix, table, ignoredColumns):
    with open(filename) as f:
        for line in f:
            print "yes"

def readTweets(api, query):
    #read all tweets that satisfy serch conditions
    return api.search(query, lang='en')
def updateStatus(api, status):
    api.update_status(status)
def sendPrivate(message, user):
    api.update_status(user+" "+message)
def getText():
    response = urllib2.urlopen('http://python.org/')
    html = response.read()

    
if __name__ == "__main__":
    api=login()
    i=1
    while i==1:
        r=random.random()
        if r<0.5:
            statuses=readTweets(api, '"my mom"')
        else:
            statuses=readTweets(api, '"my dog"')
        #getText()
        if statuses:
            for status in statuses:
                if "RT" and "@" not in status.text:
                    if "http" not in status.text:
                        if len(status.text)<120:
                            if r<0.5:
                                text=status.text.encode('ascii', 'replace').split("#")[0]
                                text=text.lower().replace("dad", "shaver")
                                print text.replace("my mom", "my twitterbot")
                                #updateStatus(api, text.replace("my mom", "my twitterbot"))
                            else:
                                text=status.text.encode('ascii', 'replace').split("#")[0]
                                print text.lower().replace("my dog", "my twitterbot")
                                #updateStatus(api, text.lower().replace("my dog", "my bot"))
                            break;
        for k in range(10):
            time.sleep(3)
            print 'tic %i' % k
    