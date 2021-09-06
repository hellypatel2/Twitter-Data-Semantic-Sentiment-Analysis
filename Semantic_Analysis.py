import json,re,math
from prettytable import PrettyTable
jsonData='{}'
tweets=[]
wordCount={}
N=3000
flu=0
cold=0
snow=0
d={}
c=0
relativeFrequency=[]

coldOccurrence	=[]
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF" "]+")
fileTweets=open("Tweet.json","r")
readTweet=fileTweets.readlines()

for l in readTweet:
     for i in json.loads(l):
         if (i == "text"):
             url = re.sub(r'http\S+', " ", json.loads(l)[i])
             letters = re.sub(r'\W+', ' ', url)
             filterd = emoji_pattern.sub(r'', letters)
             add = json.loads(jsonData)
             add.update({c:filterd})
             c=c+1
             tweets.append(add)

for i in tweets:
    for j in i:
        tweet=i[j]
        listOfWords=i[j].strip(" ").split(" ")
        for a in listOfWords:
            wordCount[a] = listOfWords.count(a)
        i[j]=wordCount
        if "flu" in i[j].keys():
            flu=flu+i[j]["flu"]
        elif "cold" in i[j].keys():
            cold=cold+i[j]["cold"]
            add = json.loads(jsonData)
            add.update({"Document": tweet})
            add.update({"Total words": len(i[j].keys())})
            add.update({"Frequency": i[j]["cold"]})
            coldOccurrence.append(add)
        elif "snow" in i[j].keys():
            snow=snow+i[j]["snow"]
        wordCount = {}
table1=PrettyTable()
table1.field_names=("Search Query", "(df)","(N=3000)/(df)","Log10(N/df)")
table1.add_row(["flu",flu,"3000"+"/"+str(flu),math.log10(N/flu)])
table1.add_row(["cold",cold,"3000"+"/"+str(cold),math.log10(N/cold)])
table1.add_row(["snow",snow,"3000"+"/"+str(snow),math.log10(N/snow)])
table2=PrettyTable()
table2.field_names=("Document","Total words","Frequency")
frequency=[]
for x in coldOccurrence:
    table2.add_row([x["Document"], x["Total words"], x["Frequency"]])
    add=json.loads(jsonData)
    add.update({"rf":x["Frequency"]/x["Total words"]})
    add.update({"tweet":x["Document"]})
    relativeFrequency.append(add)


def relative_frequency(rf):
    max = relativeFrequency[0]["rf"]
    for i in range(1,len(relativeFrequency)):
        if relativeFrequency[i]["rf"]>max:
            max=relativeFrequency[i]["rf"]
    return "Tweet with highest relative frequency= "+relativeFrequency[i]["tweet"]+ "\nwhere (f/m)="+str(max)

print(relative_frequency(relativeFrequency))
print(table1)
print(table2)
