# 💻 💰 **AI/DATA Log Traffic Handler**

This project consists of Multi Layer Perceptron (MLP), generating training data, and training an AI that decides normal, legitimate unusual and illegitimate unusual traffic.

## **Project Setup**

### **OS**

![]()<img src="https://upload.wikimedia.org/wikipedia/commons/c/c5/Pop_OS-Logo-nobg.svg" width="125" height="125">
[Pop!_OS](https://pop.system76.com/) Linux

### **Programs used**

 ![](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Elasticsearch_logo.svg/512px-Elasticsearch_logo.svg.png?20210414071206)
<img src="https://brandslogos.com/wp-content/uploads/images/large/elastic-kibana-logo.png" width="125" height="125">  **Kibana**

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2560px-Python_logo_and_wordmark.svg.png" height="125">

## Data Description

We were tasked to use the logs of our PC and we have recovered these logs present in our system files ( directory: * var/log* ) :

- dpkg.log
- kern.log
- sys.log

In computing, a log file is used to store the history of events on a server, computer or application.

### Data generation

In order to have abnormal legitimate traffic, we have generated nmaps and pings from another host to our machine.

## Data Extraction

To collect our data, we made a python script named "elastic_data.py" that first formats our data and imports it into elasticSearch.

```yarn
from elasticsearch import Elasticsearch
from datetime import datetime
import json
import re

client = Elasticsearch("http://10.78.120.44:9200")

print(client.info(), '\n')

logPath = "/var/log/"
logFiles = ["syslog", "kern.log", "dpkg.log"]

trainPath = "training_data/"
trainFolders = ["syslog/", "kern.log/"]
trainFiles = ["anormal_illegitime.txt", "anormal_legitime.txt", "normal.txt"]
```

Elasticsearch is designed to manage and support large volumes of data (several Terabytes of data if needed).

The search functionalities are powerful, they allow predictive search, text search, synonym search.

### Common data of logs

#### Logging formats

Kern.log

![](file:/kernlog pictures/unfiltered.png)

The transformation of our Kern.log

```yarn
def KernLogFormat(logString):
	logString = [x for x in logString if x]
	logYear = int(datetime.now().strftime("%Y"))
	logMonth = int(datetime.strptime(logString[0], "%b").month)
	logDay = int(logString[1])
	hours = logString[2]
	dateDatetime = datetime(logYear, logMonth, logDay)

	logTimeStamp = dateDatetime.strftime("%Y/%m/%d ") + hours
	logLevel = None
	logSystem = logString[3]
	logService = logString[4].strip(":")
	logMessage = ' '.join(logString[5:])

	return {"timestamp":logTimeStamp, 
			"log-level":logLevel,
			"system":logSystem, 
			"service":logService,
			"message":logMessage}
```

***Filtered log format***

| log-level | system | service | IN  | SRC | DST | PROTO | SPT | DPT | LEN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

![](file:/kernlog pitures/filtered.png)

## **AI Training**

### Data Filter

```yaml
def DataFilter(indexLines, train=False):
    #log-level,system,service,IN,SRC,DST,PROTO,SPT,DPT,LEN
    dataDump = []
    matches = ['IN', 'SRC', 'DST', 'LEN', 'PROTO', 'SPT', 'DPT']
```

### **targetLevels**

```yaml
if(train != False):
       targetLevels = {
           "normal": (1, 0, 0),
           "anormal_legitime": (0, 1, 0),
           "anormal_illegitime": (0, 0, 1)
       }
```

#### AI is trained to decide the traffic results through these 3 states

##### Normal, abnormally legitimate, abnormally illegitimate

We have used pings and Nmaps from another host to generate abnormally legitimate, and abnormally illegitimate traffic.

### 🧠 Neural networks

A multilayer perceptron is a fully connected class of feedforward **artificial neural networks**. It contains many perceptrons that are organized into layers.

[](https://www.ibm.com/cloud/learn/neural-networks)

```yaml
from sklearn.neural_network import MLPClassifier
```
We are using the multi-layer perceptron classifier.

![](file:/kernlog pictures/mlp.png)

```yarn
mlp = MLPClassifier(random_state=1, max_iter=300).fit(toTrainX, toTrainY)
```

It allows to train the generated dataset and therefore decide the traffic results through artificial intelligence.

