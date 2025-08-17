from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class Telemetry_data:
   time: float
   throttle: float
   brake: float
   speed: float
   tire_slippage: Optional[Tuple[float, float, float, float]] = None # RL, RR, FL, FR

   def set_tire_slippage(self, slippage: Tuple[float, float, float, float]):
      """Update tire slippage after object creation."""
      if len(slippage) != 4:
         raise ValueError("tire_slippage must be a tuple of 4 floats (RL, RR, FL, FR)")
      self.tire_slippage = slippage
