# 💻 💰 AI/DATA Project 

This project consists of creating an AI that recognises normal, legitimate unusual and illegitimate unusual activities.

## Build with 

- Python
- Kibana
- Elasticsearch

## DATA Description

We chose to use the logs of our PC. Indeed, we have recovered logs present in the files:  
- dpkg.log
- kern.log
- sys.log

In computing, a log file is used to store a history of events on a server, computer or application.

### DATA Collect

To collect our data, we made a python script named "elastic_data.py" that first formats our data and imports it into elasticSearch. Elascticsearch is designed to manage and support large volumes of data (several Tera of data if the infrastructure follows). The search functionalities are powerful, they allow predictive search, text search, synonym search.

'''
def SysLogFormat(logString):
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

	try:
		logMessage = json.loads(' '.join(logString[5:]))
	except:
		logMessage = ' '.join(logString[5:])

	if isinstance(logMessage, dict):
		logLevel = logMessage['log.level']
		logYear = eval(logMessage['@timestamp'][:4])
		dateDatetime = datetime(logYear, logMonth, logDay)
		logTimeStamp = dateDatetime.strftime("%Y/%m/%d ") + hours
		logService = logMessage['service.name']
		logMessage = logMessage['message']

	return {"timestamp":logTimeStamp, 
			"log-level":logLevel,
			"system":logSystem, 
			"service":logService,
			"message":logMessage}

'''

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


