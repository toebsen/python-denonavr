# python-denonavr

`denonavr` is a Python 3.x package that provides state information and some control of an `Denon AVR X1000` device over a network.
This is achieved via a telnet connection and the public protocol(see https://www.denon.de/de/product/hometheater/avreceivers/avrx1000?docname=AVRX1000_E300_PROTOCOL(1000)_V01.pdf)
It includes `denonavr_server`, an HTTP server to facilitate RESTful access to a denon devices.

# Current Features:
## Power
- get current power state via url/power/state
- turnOn via url/power/turnon
- turnOff via url/power/turnoff
## Volume
- get current volume via url/volume/level
- set  volume via url/set/<int:level>  e.g. http://192.168.2.241:12345/volume/set/40 will set the AVR to 40DB
## Input Source
- get current input source via url/input/state
- set input source via url/input/switch/<source_id> e.g. http://192.168.2.241:12345/input/switch/dvd
- source has to be one of ["DVD", "BD", "GAME", "SAT/CBL"]


inspired by https://github.com/happyleavesaoc/python-firetv


