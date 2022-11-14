# 💻 💰 AI/DATA Project 

This project consists of creating an AI that recognises normal, legitimate unusual and illegitimate unusual activities.

## DATA Description

We chose to use the logs of our PC. Indeed, we have recovered logs present in the files:  
- dpkg.log
- kern.log
- sys.log

In computing, a log file is used to store a history of events on a server, computer or application.

### DATA Collect

To collect our data, we made a python script that first formats our data and imports it into elasticSearch. Elascticsearch is designed to manage and support large volumes of data (several Tera of data if the infrastructure follows). The search functionalities are powerful, they allow predictive search, text search, synonym search.

## DATA Encryption


```yaml
from elasticsearch import Elasticsearch
from datetime import datetime
import json
import re
```


## AI Training 

[titre de l'image](./pics/image.png)

| titre | argument | blabla |
| :---: | ---: | :--- |
| truc 1 | truc 2 | truc 3|


