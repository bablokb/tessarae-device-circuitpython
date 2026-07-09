# ----------------------------------------------------------------------------
# Generic Tesserae Client.
#
# This client uses the REST-API to communicate with a Tesserae server.
# See https://github.com/dmellok/tesserae to learn about Tesserae.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

# --- imports   --------------------------------------------------------------

import board
import time
import atexit

from settings import app_config
from base_app.ui_application import UIApplication
from tesserae_dataprovider import DataProvider
from tesserae_uiprovider import UIProvider

# --- wait for connected console   -------------------------------------------

def wait_for_console(duration=5):
  """ wait for serial connection.
  If there is no supervisor, we are on CPython and don't have to wait.
  """
  import board
  try:
    import supervisor
    import time
    elapsed = time.monotonic() + duration
    while (not supervisor.runtime.serial_connected and
           time.monotonic() < elapsed):
      time.sleep(1)
  except:
    pass
  print(f"running on board {board.board_id}")

# --- cleanup at exit   ------------------------------------------------------

def at_exit(app):
  app.at_exit()

# --- application class with overrides   --------------------------------------

class App(UIApplication):
  """ class App """
  def __init__(self,*args,**kwargs):
    super().__init__(*args, ** kwargs)

    # fill in attributes needed by data and ui-provider
    self.data.update({
      "url":          app_config.url,
      "name":         getattr(app_config,"name", board.board_id),
      "device_id":    app_config.device_id,
      "token":        self._get_token(),
      "pairing_code": getattr(app_config,"pairing_code", None),
      "magic":        getattr(app_config, "magic", 0x4201),
      "mac":          getattr(app_config,"mac", self.wifi.mac_address),
      "width":        self.display.width,
      "height":       self.display.height,
      "gamut":        getattr(app_config, "gamut", self._map_color()),
      })

  # --- override idle-processing   --------------------------------------------

  def run_idle(self):
    """ Overriden to honor sleep_time set by data-provider """
    if "sleep_time" in self.data:
      interval = self.data["sleep_time"]
    else:
      # application default run-interval
      interval = getattr(app_config, "run_interval", 60)

    while time.monotonic()-self._run_start < interval:
      if self.process_events():
        return

  # --- get token   ----------------------------------------------------------

  def _get_token(self):
    """ get token """

    if hasattr(app_config,"token"):
      # use hard coded token
      return app_config.token
    else:
      try:
        # use token from NVRAM (TODO: move to HAL)
        import microcontroller
        if self.data["magic"] == microcontroller.nvm[0:2]:
          length = microcontroller.nvm[2]
          return (microcontroller.nvm[3:length+3]).decode()
        else:
          return None
      except:
        return None

  # --- map display-attributes to gamut   ------------------------------------

  def _map_color(self):
    """ map display-attributes """
    if hasattr(self.display, "color_depth"):
      # this is a Busdisplay
      if self.display.color_depth == 24:
        return "rgb24"
      else:
        return "rgb16"
    else:
      # this is an EPaperDisplay
      for attr, value in [("grayscale", "gray"),
                          ("advanced_color_epaper", "acep_7colour"),
                          ("spectra6", "spectra_6")]:
        if getattr(self.display, attr, False):
          return value
      return "mono"

# --- main program   ----------------------------------------------------------

if getattr(app_config,"debug",False):
  wait_for_console()

start = time.monotonic()
data_provider = DataProvider()
ui_provider = UIProvider()

app = App(data_provider,ui_provider,
          with_rtc=getattr(app_config, "with_rtc", False))
atexit.register(at_exit,app)

if getattr(app_config,"debug",False):
  print(f"startup: {time.monotonic()-start:f}s")

if not getattr(app_config,"always_on",False):
  print(f"running once")
  app.run_once()
else:
  print(f"runing endless")
  while True:
    app.run()
