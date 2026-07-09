# ----------------------------------------------------------------------------
# settings_pygame.py: Hardware-settings specific to pygame. Not maintained
#                     in repo.
#
# This file is imported by src/settings.py
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-device-circuitpython
# ----------------------------------------------------------------------------

import os
from blinka_displayio_pygamedisplay import PyGameDisplay

# display-sizes

DISPLAY_TYPES = {
  "native":      (900, 600, ("color_depth",24)),
  "what":        (400, 300, None),
  "ii4_old":     (640, 400, "advanced_color_epaper"),
  "ii4":         (600, 400, "spectra6"),
  "ii5.7_old":   (600, 448, "advanced_color_epaper"),
  "ii5.7":       (600, 448, "spectra6"),
  "ii7.3_old":   (800, 480, "advanced_color_epaper"),
  "iframe5.7":   (600, 448, "advanced_color_epaper"),
  "badger2040w": (296, 128, None),
  "sunton-2424": (240, 240, ("color_depth",16))
  }

disp_type = os.getenv("TESSERAE_DISPLAY", default="native")
width, height, gamut  = DISPLAY_TYPES[disp_type]

CAPTION = "Tesserae-Client"

class Settings:
  pass

# --- helper-function for HAL   -----------------------------------------------

def _get_display(hal):
  """ create display for pygame
  Simulates color-depth or color-attributes according to display-type.
  """

  display = PyGameDisplay(width=width,height=height,
                       caption=CAPTION,
                       auto_refresh=True,
                       refresh_on_pygame_events=True,
                       native_frames_per_second=0.5)
  if isinstance(gamut,tuple):
    display.color_depth = gamut[1]
  elif isinstance(gamut,str):
    setattr(display,gamut,True)
  return display

# hardware configuration   ---------------------------------------------------

hw_config = Settings()
hw_config.DISPLAY = _get_display
