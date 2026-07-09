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
    pip install adafruit-circuitpython-imageload

With a valid `src/settings.py`, starting the client needs:

    (cd src; TESSERAE_DISPLAY=native python3 ./main.py)

For a list of valid displays to emulate, see `src/settings_pygame.py`.


Note: all software prereqs are also available for MacOS and Windows. In
theory, the client should therefore also run on these platforms. What is
missing are HAL (hardware-abstraction-layer) files for the given platforms.
These files should be very similar to the existing HAL for Linux. Contributions
are welcome!
