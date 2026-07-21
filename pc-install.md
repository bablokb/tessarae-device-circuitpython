Installation on a Linux-PC/Laptop
=================================

The Tesserae-Client on a Linux system needs "Blinka", which provides
the CircuitPython-API, PyGame for the UI and a shim that beats PyGame
to behave (almost) as a native CircuitPython display.

Run the following commands to install the environment:

    python3 -m venv venv.tesserae.cp-client
    . venv.tesserae.cp-client/bin/activate
    pip install blinka-displayio-pygamedisplay
    pip install adafruit-circuitpython-display-text

With a valid `src/settings.py`, starting the client needs:

    (cd src; TESSERAE_DISPLAY=native python3 ./main.py)

For a list of valid displays to emulate, see `src/settings_pygame.py`.


Note: all software prereqs are also available for MacOS and Windows.
macOS is confirmed working — see [macOS Install](./mac-install.md); it
reuses the Linux HAL and needs no platform-specific HAL file. Windows
is untested but should be similar. Contributions are welcome!
