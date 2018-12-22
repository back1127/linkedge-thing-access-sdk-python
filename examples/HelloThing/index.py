# -*- coding: utf-8 -*-
import logging
import lethingaccesssdk
import time


# User need to implement this class
class Temperature_device(lethingaccesssdk.ThingCallback):
  def __init__(self):
    self.temperature = 41

  def callService(self, name, input_value):
    return -1, {}

  def getProperties(self, input_value):
    if input_value[0] == "temperature":
      return 0, {input_value[0]: self.temperature}
    else:
      return -1

  def setProperties(self, input_value):
    if "temperature" in input_value:
      self.temperature = input_value["temperature"]
      return 0, {}

device_obj_dict = {}
# User define device behavior
def device_behavior():
  while True:
    time.sleep(2)
    for client_handler in device_obj_dict:
      app_callback = device_obj_dict.get(client_handler)
      if app_callback.temperature > 40:
        client_handler.reportEvent('high_temperature', {'temperature': app_callback.temperature})
        client_handler.reportProperties({'temperature': app_callback.temperature})

try:
  driver_conf = lethingaccesssdk.getDriverConfig()
  for config in driver_conf:
    app_callback = Temperature_device()
    client_handler = lethingaccesssdk.ThingAccessClient(config)
    client_handler.registerAndonline(app_callback)
    device_obj_dict[client_handler] = app_callback
  device_behavior()
except Exception as e:
  logging.error(e)

#don't remove this function
def handler(event, context):
  logger = logging.getLogger()