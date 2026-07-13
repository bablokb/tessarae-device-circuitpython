# ----------------------------------------------------------------------------
# Dataprovider for the Generic Tesserae Client.
#
# This client uses the REST-API to communicate with a Tesserae server.
# See https://github.com/dmellok/tesserae to learn about Tesserae.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/tesserae-devive-circuitpython
# ----------------------------------------------------------------------------

import time

from settings import secrets, hw_config, app_config
from tesserae_api import Tesserae_ID, Tesserae_API

# --- main data-provider class   ---------------------------------------------

class DataProvider:

  def __init__(self):
    self._debug = getattr(app_config, "debug", False)
    self._wifi  = None
    self._api   = None

  # --- print debug-message   ------------------------------------------------

  def msg(self,text):
    """ print (debug) message """
    if self._debug:
      if isinstance(text, dict):
        print("DataProvider: {")
        for key, value in text.items():
          print(f"DataProvider:   {key}: {value}")
        print("DataProvider: }")
      else:
        print(f"DataProvider: {text}")

  # --- set wifi-object   ----------------------------------------------------

  def set_wifi(self,wifi):
    """ callback set wifi-object """
    self._wifi = wifi

  # --- create API interface   -----------------------------------------------

  def _create_api(self):
    """ create API interface """
    self.msg("creating API-interface")
    if not self._wifi.radio.connected:
      self._wifi.connect()

    self._panel = Tesserae_ID(self._data["name"],
                              self._data["device_id"],
                              self._data["width"],
                              self._data["height"],
                              self._data["format"],
                              self._data["gamut"],
                              self._data["mac"])
    self._api   = Tesserae_API(self._panel.id,
                               self._data["url"],
                               self._wifi.requests,
                               token=self._data["token"],
                               debug=self._debug)

  # --- discovery helper   ---------------------------------------------------

  def discover(self):
    """ use discovery """
    code, resp = self._api.discover()
    if code != 200:
      # bail out
      raise RuntimeError(f"Tesserae-Server HTTP-Code: {code}, content: {resp}")
    if resp.get("registered",False):
      self.msg(f"registered with token: {self._api.token}")
      self._data["token"] = self._api.token
      return 0
    else:
      return resp.get("retry_after_s",30)

  # --- register helper   --------------------------------------------------

  def register(self, pairing_code):
    """ use fallback registration """
    code, resp = self._api.register(pairing_code)
    if code != 201:
      # bail out
      raise RuntimeError(f"Tesserae-Server HTTP-Code: {code}, content: {resp}")
    self._data["token"] = self._api.token
    self.msg(
      f"registered with token: {self._api.token} (reused: {resp.reused_existing}"
    )

  # --- query data   ---------------------------------------------------------

  def update_data(self,data):
    """ callback for App: query data and update data-object """

    # this data provider follows the discover/register workflow from the
    # docs.

    # save a reference to the model
    self._data = data
    # create and cache the API interface
    if not self._api:
      self._create_api()

    # skip discovery/registration if we have a token
    if not self._data["token"]:
      if self._data["pairing_code"]:
        self.register(self._data["pairing_code"])
      else:
        wait_time = self.discover()
        if wait_time:
          # not yet registered by admin
          data["sleep_time"] = wait_time
          return

    # at this point we should have a token (or the pairing code is invalid)
    code, resp = self._api.frame()
    self.msg(f"api.frame(): HTTP-code: {code}")
    if resp:
      self.msg(resp)

    # fetch dashboard data for 200 and non e-inks
    if code == 200 or (code == 304 and
                       self._data["gamut"] in ["rgb16", "rgb24"]):
      self._data["dashboard"] = self._api.url_content()
      self.msg(f"dashboard size: {len(self._data['dashboard'])}")
    elif "dashboard" in self._data:
      del self._data["dashboard"]

    # send status (with battery information)
    code, resp = self._api.status({"battery_mv": 1000*data["bat_level"]})
    self.msg(f"api.status(): HTTP-code: {code}")
    if code == 200:
      self.msg(resp)
      data["sleep_time"] = resp.get("next_poll_s",30)
    else:
      raise RuntimeError(f"unexpected HTTP return code {code}")

    return
