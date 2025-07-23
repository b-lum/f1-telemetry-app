from telemetry_objects.lap import Lap

class Session :

   def __init__(self, id) :
      self.id = id
      self.laps = {}


   def add_lap(self, lap) :
      self.laps[lap.num] = lap
   
   def delete_lap(self, lap_num) :
      del self.laps[lap_num]