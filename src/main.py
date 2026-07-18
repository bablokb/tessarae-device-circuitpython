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
    self._token = self._get_token()
    self.data.update({
      "url":          app_config.url,
      "name":         getattr(app_config,"name", board.board_id),
      "device_id":    app_config.device_id,
      "token":        self._token,
      "pairing_code": getattr(app_config,"pairing_code", None),
      "mac":          getattr(app_config,"mac", self.wifi.mac_address),
      "width":        self.display.width,
      "height":       self.display.height,
      "format":       getattr(app_config,"format", "bmp"),
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

  # --- run at end of run()   ------------------------------------------------

  def run_end(self):
    """ Hook to execute at end of run(): save token """
    self._save_token()

  # --- get token   ----------------------------------------------------------

  def _get_token(self):
    """ get token """

    if hasattr(app_config,"token"):
      # use hard coded token
      self.msg("main: using hard-coded token")
      return app_config.token

    self._magic = getattr(app_config, "magic", 0x4201)
    self.msg(f"main: reading token from NVRAM with magic: {self._magic}")
    buffer = self._impl.nvram_read(0, 3)
    if not self._magic == int(buffer[:2].hex(),16):
      # magic number does not match, invalidate token
      self.msg("main: magic number does not match, no token read")
      return None
    else:
      # read token with given length
      return self._impl.nvram_read(3, buffer[2]).decode()

  # --- get token   ----------------------------------------------------------

  def _save_token(self):
    """ save token

    The token is saved in NVRAM as: magic-number,length,token. The magic-number
    allows to verify that we don't read random garbage and it allows to
    invalidate an old token.
    """

    if self.data["token"] == self._token:
      # not a new token, no need to save anything
      self.msg("main: not saving token (no change)")
      return
    elif self.data["token"] == None:
      # dataprovider invalidated the token, clear magic-number
      self.msg(f"token invalidated, clearing NVRAM")
      self._impl.nvram_write(0, b'\x00\x00')
      return

    # write magic-number|length|token to NVRAM
    self._token = self.data["token"]
    token = bytes(self.data["token"],'utf-8')
    buffer = bytearray(3 + len(token))
    buffer[:2] = self._magic.to_bytes(2,'big')
    buffer[2]  = len(token)
    buffer[3:3+len(token)] = token
    self.msg(f"saving '{buffer}' to NVRAM")
    self._impl.nvram_write(0, buffer)

  # --- map display-attributes to gamut   ------------------------------------

  def _map_color(self):
    """ map display-attributes.
    Important Note: auto-detection is only guesswork. Set
    app_config.gamut if this fails.
    """
    disp_type = str(type(self.display))
    if "BusDisplay" in disp_type:
      return "rgb16"
    elif "SPD1656" in disp_type:
      return "acep_7colour"
    elif "Inky_673" in disp_type:
      return "spectra_6"
    elif "PyGameDisplay" in disp_type:
      # this class exposes more attributes
      if hasattr(self.display, "color_depth"):
        if self.display.color_depth == 24:
          return "rgb24"
        else:
          return "rgb16"
      else:
        for attr, value in [("grayscale", "gray_4"),
                            ("advanced_color_epaper", "acep_7colour"),
                            ("spectra6", "spectra_6")]:
          if getattr(self.display, attr, False):
            return value
        return "mono"
    else:
      # fallback to mono
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
