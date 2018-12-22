# -*- coding: utf-8 -*-
import logging
import lethingaccesssdk
import time


class Light_Sensor(lethingaccesssdk.ThingCallback):
  def __init__(self):
    self.MeasuredIlluminance = 100

  def callService(self, name, input_value):
    return -1, {}

  def getProperties(self, input_value):
    if input_value[0] == "MeasuredIlluminance":
      return 0, {input_value[0]: self.MeasuredIlluminance}
    else:
      return -1, {}

  def setProperties(self, input_value):
    if "MeasuredIlluminance" in input_value:
      self.MeasuredIlluminance = input_value["MeasuredIlluminance"]
      return 0, {}

device_obj_dict = {}
# User define device behavior
def device_behavior():
  while True:
    time.sleep(1)
    for client_handler in device_obj_dict:
      light_sensor = device_obj_dict.get(client_handler)
      propertiesDict={"MeasuredIlluminance":light_sensor.MeasuredIlluminance}
      client_handler.reportProperties(propertiesDict)
      if light_sensor.MeasuredIlluminance == 600:
        light_sensor.MeasuredIlluminance = 100
      else:
        light_sensor.MeasuredIlluminance = light_sensor.MeasuredIlluminance + 100

try:
  driver_conf = lethingaccesssdk.getDriverConfig()
  for config in driver_conf:
    light_sensor = Light_Sensor()
    client_handler = lethingaccesssdk.ThingAccessClient(config)
    client_handler.registerAndonline(light_sensor)
    device_obj_dict[client_handler] = light_sensor
  device_behavior()
except Exception as e:
  logging.error(e)
  
def handler(event, context):
  
  return 'hello world'
