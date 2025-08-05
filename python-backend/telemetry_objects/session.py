from telemetry_objects.lap import Lap
from collections import deque

class Session :

   def __init__(self, session_id):
      self.laps = {}
      self.session_id = session_id

   # takes in lap_object
   def add_lap(self, lap) :
      self.laps[lap.lap_number] = lap
