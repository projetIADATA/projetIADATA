from sklearn.neural_network import MLPClassifier
from elasticsearch import Elasticsearch
import sys
import pandas as pd

#normal, anormal légitime, anormal illégitime
#(1, 0, 0)  (0, 1, 0)   (0, 0, 1)

def DataFilter(indexLines, train=False):
    #log-level,system,service,IN,SRC,DST,PROTO,SPT,DPT,LEN
    dataDump = []
    matches = ['IN', 'SRC', 'DST', 'LEN', 'PROTO', 'SPT', 'DPT']

    for line in indexLines:
        line = line['_source']
        del line['timestamp']

        if all(x in str(line['message']) for x in matches):
            messageSplit = line['message'].strip().split(" ")
            #print(messageSplit, end='\r')
            for split in messageSplit:
                for match in matches:
                    if (match == split.split("=")[0]):
                        line[match] = split.lstrip(match).strip('=')
            line['message'] = None
            if('10.78.120.' in line['SRC']):
                line['SRC'] = 'INTERNAL'
            else:
                line['SRC'] = 'EXTERNAL'
            if('10.78.120.' in line['DST']):
                line['DST'] = 'INTERNAL'
            else:
                line['DST'] = 'EXTERNAL'

        else:
            line['IN'] = 'None'
            line['SRC'] = 'None'
            line['DST'] = 'None'
            line['LEN'] = 'None'
            line['PROTO'] = 'None'
            line['SPT'] = 'None'
            line['DPT'] = 'None'

        for key in line:
            line[key] = key+"="+str(line[key])
        dataDump.append(line)

    if(train != False):
        targetLevels = {
            "normal": (1, 0, 0),
            "anormal_legitime": (0, 1, 0),
            "anormal_illegitime": (0, 0, 1)
        }

        targets = [targetLevels[train]] * len(dataDump)
        return dataDump, targets

    return dataDump

trainIndexes = ["kern.log-anormal_illegitime.txt", "kern.log-anormal_legitime.txt", "syslog-anormal_illegitime.txt", "syslog-anormal_legitime.txt"] # "kern.log-normal.txt", "syslog-normal.txt"
dataIndexes = ["kern.log", "syslog", "dpkg.log"]

toTrainX = []
toTrainY = []
toAnalyze = []

client = Elasticsearch("http://10.78.120.44:9200")
for index in dataIndexes:
    client.indices.put_settings(index=index, body= {"index" : {"max_result_window" : 500000}})
for index in trainIndexes:
    client.indices.put_settings(index=index, body= {"index" : {"max_result_window" : 500000}})
print(sys.maxsize)
print(client.info(), '\n')

for index in dataIndexes:
    i = 0
    while True:
        resp = client.search(index=index, query={"match_all": {}}, size=500000, from_=i)
        if(resp['hits']['total']['value'] == 500000):
            i += 500000
            toAnalyze.extend(DataFilter(resp['hits']['hits']))
        else:
            toAnalyze.extend(DataFilter(resp['hits']['hits']))
            break


for index in trainIndexes:
    trainType = index.split("-")[1].rstrip(".txt")
    i = 0
    while True:
        resp = client.search(index=index, query={"match_all": {}}, size=500000, from_=i)
        if(resp['hits']['total']['value'] == 500000):
            i += 500000
            trainX, trainY = DataFilter(resp['hits']['hits'], train=trainType)
            toTrainX.extend(trainX)
            toTrainY.extend(trainY)
        else:
            trainX, trainY = DataFilter(resp['hits']['hits'], train=trainType)
            toTrainX.extend(trainX)
            toTrainY.extend(trainY)
            break


toTrainX = pd.DataFrame(toTrainX)
print(toTrainX)
toTrainX = pd.get_dummies(toTrainX) #columns=['log-level', 'system', 'service', 'message', 'IN', 'SRC', 'DST', 'LEN', 'PROTO', 'SPT', 'DPT']
print(toTrainX)

mlp = MLPClassifier(random_state=1, max_iter=300).fit(toTrainX, toTrainY)

toAnalyze = pd.DataFrame(toAnalyze)
print(toAnalyze)
toAnalyze = pd.get_dummies(toAnalyze) #columns=['log-level', 'system', 'service', 'message', 'IN', 'SRC', 'DST', 'LEN', 'PROTO', 'SPT', 'DPT']
print(toAnalyze)