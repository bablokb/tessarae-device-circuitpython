Generic Tesserae Device Firmware
================================

**WORK IN EARLY PROGRESS**

Overview
--------

This repository implements a [Tesserae](https://github.com/dmellok/tesserae)
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

See [PC/Laptop Install](./pc-install.md) for how to install this client
on a Linux-PC.

See [macOS Install](./mac-install.md) for how to install this client
on a Mac. No macOS-specific HAL is needed: forcing Blinka to identify
as a generic Linux-PC lets the existing `GENERIC_LINUX_PC` HAL be
reused unchanged.

See [CircuitPython Device Install](./mcu-install.md) for how to install
this client on a MCU.


Configuration
-------------

The central configuration file is `src/settings.py` which is not
tracked by the repository. Copy the blueprint `src/settings_template.py`
to `src/settings.py` and edit where appropriate.

The file creates three `Settings`-objects:

  - `secrets`: WLAN credentials (only needed for real hardware)
  - `app_config`: application configuration
  - `hw_config`: hardware configuration

Use one of the examples in `contrib/` as a basis for the necessary
hardware configuration. Either merge the example into your
`settings.py`, or create `src/local`, copy the example to `src/local`
and add an import statement to your `settings.py`:

    from local.bla import hw_config

Note that `src/local` is not tracked by git, these files are local to
your clone. If you create a useful hardware-config file, copy it to
`contrib/` and create a PR.


Examples
--------

Some examples and screenshots are (i.e. will be) in `examples/`.


Contributing
------------

For new HAL files for specific hardware boards create a PR in the
Base App repo.

To add a configuration layer example, create a PR here.
