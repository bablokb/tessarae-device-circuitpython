Generic Tessarae Device Firmware
================================

**WORK IN EARLY PROGRESS**

Overview
--------

This repository implements a [Tessarae](https://github.com/dmellok/tesserae)
client using CircuitPython.

CircuitPython runs on as of today 655 boards. It also runs on a normal
laptop/PC using Blinka. So the rationale of this project is to provide
a generic client that runs on all boards that support CircuitPython and
are powerful enough to drive a display.

This repository uses at it's core the [CircuitPython Base
App](https://github.com/bablokb/circuitpython-base-app) that provides
the logic to pull data, update a display and go to sleep (or shutdown)
afterwards.

While CircuitPython already provides a stable API across architectures
and boards, two additional levels of abstraction are necessary. A
*hardware abstraction layer* (HAL) and a *configuration layer*. The
HAL will deal with board-specific peripherals (e.g. buttons, low-power
electronics), while the configuration layer allows a given board to run
with different displays.

The core take away is: this client will not automagically run on any
device. But to make it run, it is only necessary to create the HAL
and/or a suitable configuration.


Installation
------------

TBD


Configuration
-------------

TBD


Examples
--------

Some examples and screenshots are (i.e. will be) in `examples/`.


Contributing
------------

For new HAL files for specific hardware boards create a PR in the
Base App repo.

To add a configuration layer example, create a PR here.
