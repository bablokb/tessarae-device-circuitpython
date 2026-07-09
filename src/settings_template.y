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
app_config.app_name     = "tesserae_device_cp"
app_config.debug        = True     # needed to print the token for now
app_config.always_on    = True     # should be off when running on batteries
app_config.with_rtc     = False    # needed for local scheduling

# application specific
app_config.url       = "http://tesserae.local:8765"
app_config.name      = "CP-Test"
#app_config.gamut    = "mono"      # overrides auto-detection

#app_config.pairing_code =         # untested
#app_config.magic =                # invalidates a stored token (not impl. yet)

app_config.device_id = "cp_test_pygame"
app_config.token = None            # paste token after registration here for now
