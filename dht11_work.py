import subprocess
import re
import json
import time
import requests

from yeelinkclient import *
from ubidots import ApiClient

YEELINK_API_KEY = 'YOUR_YEELINK_API_KEY'
YEELINK_DEVICE_ID = "YOUR_DEVICE_ID"
YEELINK_SENSOR_ID_HUMIDITY = "YOUR_SENSOR_ID_1"
YEELINK_SENSOR_ID_TEMPERATOR= "YOUR_SENSOR_ID_2"

UBIDOTS_API_KEY_TOKEN = 'YOUR_UBIDOTS_TOKEN'
UBIDOTS_VARIABLE_TEMP = 'YOUR_VARIABLE_1'
UBIDOTS_VARIABLE_HUM = 'YOUR_VARIABLE_2'


def yeelink_send(hum_value, temp_value):
  client = YeelinkClient(apikey=YEELINK_API_KEY)
  hum_op = DataOperation(conn=client, deviceid=YEELINK_DEVICE_ID, sensorid=YEELINK_SENSOR_ID_HUMIDITY)
  hum_op.send_data_value(hum_value)
  temp_op = DataOperation(conn=client, deviceid=YEELINK_DEVICE_ID, sensorid=YEELINK_SENSOR_ID_TEMPERATOR)
  temp_op.send_data_value(temp_value)


def yeelink_send_onestep(hum_value, temp_value):
  client = YeelinkClient(apikey=YEELINK_API_KEY)
  md_op = MutipleDataOperation(conn=client, deviceid=YEELINK_DEVICE_ID)
  raw_data_hum = {'sensor_id': YEELINK_SENSOR_ID_HUMIDITY, 'value': hum_value}
  raw_data_temp = {'sensor_id': YEELINK_SENSOR_ID_TEMPERATOR, 'value': temp_value}
  md_op.send_data([raw_data_hum, raw_data_temp])


def ubidots_send(hum_value, temp_value):
  api = ApiClient(token=UBIDOTS_API_KEY_TOKEN)
  post_data_ubi = [{'variable': UBIDOTS_VARIABLE_TEMP, 'value':temp_value}, {'variable': UBIDOTS_VARIABLE_HUM, 'value':hum_value}]
  api.save_collection(post_data_ubi)

 
def hum_temp_process():
  #to get the humidity and temperature readings!
  output = subprocess.check_output(["./dht11"]);
  matches = re.search("Temp=([0-9.]+)C", output)
  if (not matches):
    time.sleep(3)
    return 1
  temp = float(matches.group(1))
   
  # search for humidity printout
  matches = re.search("Hum=([0-9.]+)\%", output)
  if (not matches):
    time.sleep(3)
    return 1
  humidity = float(matches.group(1))
 
  strftime = time.strftime("%Y-%m-%dT%H:%M:%S")
  datastr = "; Temperature: %.1f C; Humidity: %.1f %%; " % (temp, humidity)
  postresult = ""
  
  try:

    # upload to yeelink
    yeelink_send_onestep(hum_value=humidity, temp_value=temp)
    postresult = "Post to yeelink success!"

    # upload to ubidots
    ubidots_send(hum_value=humidity, temp_value=temp)
    postresult += ", Post to ubidots success!\n"
  
  except:
    postresult = "Unable to post data.  Check your connection?\n"
    return 2
  
  # local_log
  log_filename = "./log/%s_upload.log" % time.strftime("%Y_%m_%d")
  with open(log_filename, 'a+') as f: 
    f.write(strftime)
    f.write(datastr) 
    f.write(postresult)

  return 0

# Continuously append data
while(True):
  r = hum_temp_process()
  if r==1:
    continue
  # Wait seconds before continuing
  time.sleep(20)