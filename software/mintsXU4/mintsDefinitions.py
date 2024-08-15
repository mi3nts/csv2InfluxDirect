
from getmac import get_mac_address
import serial.tools.list_ports
import yaml
import pandas as pd
# Change Accordingly  
mintsDefinitions          = yaml.load(open('mintsXU4/credentials/mintsDefinitions.yaml'),Loader=yaml.FullLoader)
dataFolder                = mintsDefinitions['dataFolder']+ "/raw"
dataFolderReference       = mintsDefinitions['dataFolder'] + "/reference"
dataFolderMQTTReference   = mintsDefinitions['dataFolder'] + "/referenceMqtt"  # The path of your MQTT Reference Data 
dataFolderMQTT            = mintsDefinitions['dataFolder'] + "/rawMqtt"        # The path of your MQTT Raw Data 
tlsCert                   = mintsDefinitions['tlsCert']     # The path of your TLS cert

latestOn                  = False

mqttOn                    = False
credentialsFile           = 'mintsXU4/credentials/credentials.yaml'
credentials               = yaml.load(open(credentialsFile))

nodeInfo                  = pd.read_csv('https://raw.githubusercontent.com/mi3nts/AirQualityAnalysisWorkflows/main/influxdb/nodered-docker/id_lookup.csv')
sensorInfo                = pd.read_csv('https://raw.githubusercontent.com/mi3nts/mqttSubscribersV2/main/lists/sensorIDs.csv')
print(sensorInfo)

mqttBrokerDC              = "mqtt.circ.utdallas.edu"

mqttPort                  = 8883  # Secure port

macAddress                = "mtid001"


# Replace with your own InfluxDB details
# org    = "MINTS"
# bucket = "SharedAirDFW"
# token  = "RNvuscANJ5GriZxFNepL7qOPa7xDntAIh8TH2-PUXd4ACvUqW6NHuSXxDDsCc569tdcZc6fAD3SSqneKsp1OgA=="
# # 
# # url = f"http://mdash.circ.utdallas.edu:8086/api/v2/query?org={org}"
# url =  "http://mdash.circ.utdallas.edu:8086"

print()
print("----- CSV 2 Influx Direct -----")
print(" ")

# Add a few more lines 

print("Node Info:")
print(nodeInfo)
