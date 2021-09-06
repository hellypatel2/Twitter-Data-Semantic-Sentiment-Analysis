import json,re
from prettytable import PrettyTable
fileNegative=open("negative-words.txt","r")
filePositive=open("positive-words.txt","r")
fileTweets=open("Tweet.json","r")

readTweet=fileTweets.readlines()
readNegative=fileNegative.readlines()
readPositive=filePositive.readlines()
cleanTweets=open("cleanTweets.json","w")


positive=[]
negative=[]
tweetWords=[]
dict={}
listofdict=[]
d = {}
list=[]
json_data='{}'
dict_clean_tweets={}
detailsPositive=[]
detailsNegative=[]
neturalWord=[]
detailsNetural=[]

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF" "]+")

for i in readNegative:
    negative.append(i.strip("\n"))
for i in readPositive:
    positive.append(i.strip("\n"))

def polarity(tweet):
    wordCount = {}
    count=1
    positiveWord=[]
    negativeWord=[]
    netural=[]
    url = re.sub(r'http\S+', " ", tweet)
    letters = re.sub(r'\W+', ' ', url)
    filterd = emoji_pattern.sub(r'', letters)
    list_of_words = filterd.strip(" ").split(" ")

    d["tweet"] = filterd
    for a in list_of_words:
        wordCount[a] = list_of_words.count(a)

    for dict_word in list_of_words:
        d["words"] = wordCount
        if dict_word in positive:
            positiveWord.append(dict_word)
        if dict_word in negative:
            negativeWord.append(dict_word)

    if len(positiveWord)>0:
        add = json.loads(json_data)
        add.update({"word": positiveWord})
        add.update({"polarity": "positive"})
        add.update({"Tweet": d["tweet"]})
        detailsPositive.append(add)
    if len(negativeWord)>0:
        add = json.loads(json_data)
        add.update({"word": negativeWord})
        add.update({"polarity": "negative"})
        add.update({"Tweet": d["tweet"]})
        detailsNegative.append(add)

    wordCount = {}
    for i in d:
        print(i+":",d[i])


for l in readTweet:
     for i in json.loads(l):
         if (i == "text"):
             polarity(json.loads(l)[i])

for j in detailsPositive:
    for k in detailsNegative:
        if j["Tweet"]==k["Tweet"]:
            detailsPositive.remove(j)
            detailsNegative.remove(k)
            neturalWord.append(j["word"])
            neturalWord.append(k["word"])
            add = json.loads(json_data)
            add.update({"word": neturalWord})
            add.update({"polarity": "netural"})
            add.update({"Tweet": j["Tweet"]})
            detailsNetural.append(add)
            neturalWord=[]

table=PrettyTable()

table.field_names=("Tweet", "Match", "Polarity")
for z in detailsNetural:
    tweet = z["Tweet"]
    words = z["word"]
    p = z["polarity"]
    table.add_row([tweet, words, p])

for x in detailsPositive:

    tweet=x["Tweet"]
    words=x["word"]
    p=x["polarity"]
    table.add_row([tweet,words ,p ])

for y in detailsNegative:
    tweet = y["Tweet"]
    words = y["word"]
    p = y["polarity"]
    table.add_row([tweet, words, p])

print(table)

