# -*- coding: utf-8 -*-
import logging
import lethingaccesssdk
import time


class Light_Device(lethingaccesssdk.ThingCallback):
  def __init__(self):
    self.LightSwitch = 1

  def callService(self, name, input_value):
    if name == "turn":
      print(input_value["LightSwitch"])
      if input_value["LightSwitch"] == 0:
        print("turn off light")
        self.LightSwitch = 0
      else:
        print("turn on light")
        self.LightSwitch = 1
      return 0, {}
    return -1, {}


  def getProperties(self, input_value):
    if input_value[0] == "LightSwitch":
      return 0, {input_value[0]: self.LightSwitch}
    else:
      return -1, {}

  def setProperties(self, input_value):
    if "LightSwitch" in input_value:
      self.LightSwitch = input_value["LightSwitch"]
      return 0, {}

device_obj_dict = {}
# User define device behavior
def device_behavior():
  while True:
    time.sleep(1)
    for client_handler in device_obj_dict:
      light_callback = device_obj_dict.get(client_handler)
      propertiesDict={"LightSwitch":light_callback.LightSwitch}
      client_handler.reportProperties(propertiesDict)

try:
  driver_conf = lethingaccesssdk.getDriverConfig()
  for config in driver_conf:
    light_callback = Light_Device()
    client_handler = lethingaccesssdk.ThingAccessClient(config)
    client_handler.registerAndonline(light_callback)
    device_obj_dict[client_handler] = light_callback
  device_behavior()
except Exception as e:
  logging.error(e)
  
def handler(event, context):
  return 'hello world'