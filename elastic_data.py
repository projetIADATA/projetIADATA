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

#formatage des SysLog
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

#formatage des KernLog	
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
	
#formatage des DpkgLog	
def DpkgLogFormat(logString):
	logTimeStamp = logString[0].replace("-", "/") + " " + logString[1]
	logLevel = None
	logSystem = logString[2]

	if(logSystem == 'status'):
		logService = logString[4]
		logMessage = ' '.join(logString[3:])
	else:
		logService = logString[3]
		logMessage = ' '.join(logString[3:])

	return {"timestamp":logTimeStamp, 
			"log-level":logLevel,
			"system":logSystem, 
			"service":logService,
			"message":logMessage}


# for fileName in logFiles:
# 	logFilePath = logPath + fileName
# 	print(logFilePath)
# 	with open(logFilePath, 'r') as f:
# 		i = 0
# 		for line in f.readlines():
# 			print(i, end='\r')
# 			readLine = line.strip().split(" ")
# 			try:
# 				if(fileName == "syslog"):
# 					lineDict = SysLogFormat(readLine)
# 					#print(lineDict)
# 				elif(fileName == "kern.log"):
# 					lineDict = KernLogFormat(readLine)
# 					#print(lineDict)
# 				elif(fileName == "dpkg.log"):
# 					lineDict = DpkgLogFormat(readLine)
# 					#print(lineDict)
# 			except:
# 				print("err", i+1, ":", line)

# 			client.index(index=fileName, document=lineDict)
# 			i += 1


for folderName in trainFolders:
	for fileName in trainFiles:
		indexName = (folderName + fileName).replace("/", "-")
		trainFilePath = trainPath + folderName + fileName
		print(trainFilePath)
		with open(trainFilePath, 'r') as f:
			i = 0
			for line in f.readlines():
				print(i, end='\r')
				readLine = line.strip().split(" ")
				try:
					if(folderName == "syslog/"):
						lineDict = SysLogFormat(readLine)
						#print(lineDict)
					elif(folderName == "kern.log/"):
						lineDict = KernLogFormat(readLine)
						#print(lineDict)
				except:
					print("err", i+1, ":", line)

				client.index(index=indexName, document=lineDict)
				i += 1
	

"""
client.index(index='lord-of-the-rings', document={
  					'character': 'Aragon',
  					'quote': 'It is not this day.'
 					})
"""
