# ----------------------------------------------------------------------------
# settings_template.py: template for settings.py
#
# Copy this file to settings.py and adapt to your needs.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-base-app
# ----------------------------------------------------------------------------

import os
import board
if board.board_id == "GENERIC_LINUX_PC":
  from settings_pygame import hw_config

class Settings:
  pass

# network configuration (ignored for PC/laptops)   ---------------------------

secrets = Settings()
secrets.ssid      = 'my-ssid'
secrets.password  = 'my-secret-password'
secrets.retry     = 2
secrets.debugflag = False
secrets.channel   = 6
secrets.timeout   = 10
secrets.net_update = False

# app configuration   --------------------------------------------------------

# generic
app_config = Settings()
app_config.debug        = True     # needed to print the token for now
app_config.always_on    = True     # should be off when running on batteries
app_config.with_rtc     = False    # needed for local scheduling

# application specific
app_config.url       = "http://tesserae.local:8765"
#app_config.gamut    = "mono"      # overrides auto-detection
#app_config.pairing_code =         # untested
#app_config.magic =                # invalidates a stored token

# for emulation: add various settings according to display-type
#                this allows simulating multiple displays in parallel
disp_type = os.getenv("TESSERAE_DISPLAY")

if disp_type is None:
  # real hardware
  app_config.name = "CP-Client"
  #app_config.mac = ...

else:
  # emulation
  app_config.app_name  = f"Tesserae-{disp_type}"
  app_config.device_id = f"cp_{disp_type}"
  app_config.name      = f"CP-Client-{disp_type}"
  if disp_type == "ii4_old":
    # use auto-detected mac, not available on macOS
    pass
  elif disp_type == "native":
    app_config.mac = "DE:AD:BE:EF"
  elif disp_type == "sharp400":
    app_config.mac = "DE:AD:BE:EE"
