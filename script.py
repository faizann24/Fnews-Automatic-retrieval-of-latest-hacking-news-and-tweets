from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import re
import requests
import urllib2
reload(sys)
sys.setdefaultencoding('utf-8')


consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
filepath = 'your file path'

listOfTweets = []
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

class StdOutListener(StreamListener):
    def on_status(self, status):    #on getting the status
        data = open(filepath,'a')   #open the file you want to write the data in
        s = status.text     #get the text of the status
        statuss = s.encode("utf-8") 
        statuss = str(statuss)  #convert to a string
        middleText = '' #some middle text that will be used to check whether this tweet has appeared before
        isAscii = is_ascii(statuss) #check whether the text contains any other weird language

        if len(statuss) > 60:   #ignoring very short tweets since they usually don't contain enough description and url
            middleText = statuss[40:len(statuss)-20]    #getting some middle text
            isPrintable = True  #if it has not appeared before, it is printable
            for l in listOfTweets:
                if middleText in l: #checking all previous tweets to see if this tweet is new or old
                    isPrintable = False
            if isPrintable == True:
                #checking if it is related to porn. only print if it is not.
                if ('nude' not in statuss and 'sex' not in statuss and 'porn' not in statuss and 'adult' not in statuss) and ('https://t.co/' in statuss) and (isAscii == True):
                    print statuss   #printing it
                    url = str(re.findall(r'(https?://\S+)', statuss)[0])    #getting url from the tweet
                    created_at = str(status.created_at) #date of creation of tweet
                    page = opener.open(url)
                    url = str(page.geturl())    #getting the redirected url of the tweet i.e the actual source or the news url
                    data.write('"' + statuss + '","' + url + '","' + created_at + '"\n')  #writing everything in file        
            listOfTweets.append(statuss)    #appending it in a list so that we can cater it if the same tweet comes again
        data.close()
        return True

    def on_error(self, status):
        print status


l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
stream = Stream(auth, l)

#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
while True:
    try:
        stream.filter(track=['hacking tool','sql injection','website hacked','accounts hacked','hacked','password hacked','security breach','database breach','database hacked','passwords hacked','password breach','hacking attack','DDOS attack','phishing attack','company hacked'])
    except Exception as e:
        print e
