# Read CSV 
# Report Time in GMT 
# import pandas as pd
import time 
import site
import sys
import csv
from collections import OrderedDict
from mintsXU4 import mintsLatest as mL
# from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsSensorReader as mSR
import datetime 


import random


def main():

    while True:
        try:
            dateTime = datetime.datetime.now(datetime.timezone.utc)
            print(dateTime)
            MTS002Write(dateTime)
            time.sleep(1)
  
  
        except Exception as e:
            print(e)
            line = []




def MTS002Write(dateTime):

    sensorName = "MTS002"
    sensorDictionary =  OrderedDict([
                ("dateTime"          ,str(dateTime.strftime('%Y-%m-%d %H:%M:%S.%f'))),
        		("temperature"       ,25 + random.random()*5),
                ("temperatureUnits"  ,"C"),
            	("pressure"          ,900 + random.random()*10),
                ("pressureUnits"     ,"Mili Bar")
                ])

        #Getting Write Path
    mSR.sensorFinisher(dateTime,sensorName,sensorDictionary)




if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()