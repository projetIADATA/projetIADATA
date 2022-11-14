# 💻 💰 **AI/DATA Log Traffic Handler**

This project consists of Natural Language Processing, generating training data, and training an AI that decides normal, legitimate unusual  and illegitimate unusual activities.

## **Project Setup**
### **OS**
![]()
<img src="https://upload.wikimedia.org/wikipedia/commons/c/c5/Pop_OS-Logo-nobg.svg" width="125" height="125">
[Pop!_OS](https://pop.system76.com/) Ubuntu-based

### **Programs used**

![](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Elasticsearch_logo.svg/512px-Elasticsearch_logo.svg.png?20210414071206)
<img src="https://brandslogos.com/wp-content/uploads/images/large/elastic-kibana-logo.png" width="125" height="125">  **Kibana**

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2560px-Python_logo_and_wordmark.svg.png" height="125">


## Data Description

We were tasked to use the logs of our PC and we have recovered logs present in our system files:
- dpkg.log
- kern.log
- sys.log

In computing, a log file is used to store the history of events on a server, computer or application.

### Data generation

In order to have abnormally illegitimate traffic, we have generated nmaps and pings from another host to our machine.

## Data Extraction

To collect our data, we made a python script named "elastic_data.py" that first formats our data and imports it into elasticSearch.

Elasticsearch is designed to manage and support large volumes of data (several Terabytes of data if needed).

The search functionalities are powerful, they allow predictive search, text search, synonym search.

### Common data of logs
#### Data Filter
```yaml
def DataFilter(indexLines, train=False):
    #log-level,system,service,IN,SRC,DST,PROTO,SPT,DPT,LEN
    dataDump = []
    matches = ['IN', 'SRC', 'DST', 'LEN', 'PROTO', 'SPT', 'DPT']
```

#### Logging format
[Syslog format](https://www.rfc-editor.org/rfc/rfc5424#section-6)

***Filtered log format***

| log-level | system | service | IN | SRC | DST | PROTO | SPT | DPT | LEN |
| --------- | ------ | ------- | -- | --- | --- | ----- | --- | --- | --- |




## **AI Training**
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
Pings and Nmaps

### 🧠 Neural networks

[!["NN"](https://1.cms.s81c.com/sites/default/files/2021-01-06/ICLH_Diagram_Batch_01_03-DeepNeuralNetwork-WHITEBG.png)](https://www.ibm.com/cloud/learn/neural-networks)

### :desktop_computer: Natural Language Processing

[titre de l'image](./pics/image.png)

| titre | argument | blabla |
| :---: | ---: | :--- |
| truc 1 | truc 2 | truc 3|

[!
(https://www.rapid7.com/blog/post/2017/05/24/what-is-syslog/)]



```yaml
from elasticsearch import Elasticsearch

```

```yaml
from elasticsearch import Elasticsearch
from datetime import datetime
import json
import re
```
### Formats
#### Syslog
```yaml
from elasticsearch import Elasticsearch
```
