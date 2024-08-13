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
            MTS001Write(dateTime)
            time.sleep(1)
  
  
        except Exception as e:
            print(e)
            line = []
    ser.close()



def MTS001Write(dateTime):

    sensorName = "MTS001"
    sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("temperature"  , 25 + random.random()*5),
            	("pressure"     ,900 + random.random()*10)
                ])

        #Getting Write Path
    mSR.sensorFinisher(dateTime,sensorName,sensorDictionary)




if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()