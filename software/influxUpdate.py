# Import tkinter and webview libraries
from fileinput import filename
from tkinter import *
from traceback import print_stack
# import webview
import glob
import serial
import datetime
# from mintsXU4 import mintsSensorReader as mSR
# from mintsXU4 import mintsDefinitions as mD
import time
# import serial
# import pynmea2
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
# import mintsLatest as mL
import csv
import os 
# import nmap, socket
import yaml
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS 

import sys
import yaml
import os
import time
import glob


from datetime import date, timedelta, datetime
from mintsXU4 import mintsDefinitions as mD

#  With on board sensors:
    # Node ID should be updated 
    # Some means to check if connectivity is there 
    # How long should I go back to 
    # How often to send 
    # Check if already synced 



nodeInfo           = mD.nodeInfo
sensorInfo         = mD.sensorInfo


dataFolder         = mD.dataFolder

nodeIDs            = nodeInfo['mac_address']
nodeNames          = nodeInfo['name']

sensorIDs          = sensorInfo['sensorID']
credentials        = mD.credentials

influxToken        = credentials['influx']['token']  
influxOrg          = credentials['influx']['org'] 
influxBucket       = credentials['influx']['bucket'] 
influxURL          = credentials['influx']['url']

print()
print("MINTS")
print()

delta      = timedelta(days=1)

def directoryCheckV2(outputPath):
    isFile = os.path.isfile(outputPath)
    if isFile:
        return True
    if outputPath.find(".") > 0:
        directoryIn = os.path.dirname(outputPath)
    else:
        directoryIn = os.path.dirname(outputPath+"/")

    if not os.path.exists(directoryIn):
        print("Creating Folder @:" + directoryIn)
        os.makedirs(directoryIn)
        return False
    return True;


def isFloat(value):
    try:
        output = float(value)

        return output
    except ValueError:
        return value
    
def syncData2Influx(nodeID,nodeName,sensorID):
    # print(dataFolder  + "/" + nodeID + "/" + "/*/*/*/*"+sensorID+"*.csv")
    csvDataFiles = glob.glob(\
                    dataFolder  + "/" +  nodeID + "/*/*/*/*"+sensorID+"*.csv")
    csvDataFiles.sort()
    # print(csvDataFiles)

    for csvFile in csvDataFiles:
        # print("================================================")
        print("Syncing "+ csvFile)
        sendCSV2Influx(csvFile,nodeID,sensorID,nodeName)
   

def sendCSV2Influx(csvFile,nodeID,sensorID,nodeName):
    # try:
    sequence = []
    tag_columns = ["device_id", "device_name"]
    time_column = "dateTime"

    with open(csvFile, "r") as f:
        reader            = csv.DictReader((line.replace('\0','') for line in f) )
        rowList           = list(reader)
        for rowData in rowList:
            dateTimeRow = datetime.strptime(rowData['dateTime'],'%Y-%m-%d %H:%M:%S.%f')
            point = Point(sensorID)  # Replace with your measurement name
            point.tag("device_id", nodeID)
            point.tag("device_name", nodeName)
            point.time(dateTimeRow, WritePrecision.NS) 
            
            # Dynamically add fields based on the headers
            for header in reader.fieldnames:
                if header not in tag_columns and header != time_column:
                    point.field(header, isFloat(rowData[header]))
                    sequence.append(point)



        with InfluxDBClient(url=influxURL, token=influxToken, org=influxOrg) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(influxBucket, influxOrg, sequence)

            


def main():    
    for index, nodeID in enumerate(nodeIDs):
        nodeName = nodeNames[index]
        # print(f"Index: {index}, Node ID: {nodeID}, Node Name: {nodeName}")
        for sensorID in sensorIDs:
            # print("Sending data to Influx for Node ID: " + nodeID + ", Node Name: " + nodeName + ", Sensor ID: " +sensorID) 
            syncData2Influx(nodeID,nodeName,sensorID)

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()