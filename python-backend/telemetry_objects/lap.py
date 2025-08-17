from telemetry_objects.telemetry_data import Telemetry_data
from collections import deque

class Lap :

   def __init__(self, lap_number):
      self.data = {}
      self.lap_number = lap_number
      self.lap_time = None
   
   # accepts telemetry_data object
   def add_data(self, data) :
      self.data[data.time] = data
   
   # return array with averages [speed, throttle, brake]
   def get_avg(self) :
      total_speed = 0
      total_throttle = 0
      total_brake = 0

      for time in self.times() :
         total_speed += self.data[time].speed
         total_throttle += self.data[time].throttle
         total_brake += self.data[time].brake
      
      return [total_speed, total_throttle, total_brake] / len(self.times)
   
   def set_lap_time(self, lap_time) :
      self.lap_time = lap_time
