[![Build Status](https://travis-ci.com/toebsen/python-denonavr.svg?branch=master)](https://travis-ci.com/toebsen/python-denonavr.svg?branch=master)

# python-denonavr

`denonavr` is a Python 3.x package that provides state information and some control of an `Denon AVR X1000` device over a network.
This is achieved via a telnet connection and the [public protocol][1]

It includes `denonavr_server`, an HTTP server to facilitate RESTful access to a denon devices.

# Installing
1. Via source 
```
    git clone https://github.com/toebsen/python-denonavr.git
    cd python-denonavr
    pip install -r requirements.txt
    python setup.py install
    denonavr_server -p 5567
```

2. Via docker
```
    docker run --rm -p 5567:5567 toebsen/python-denonavr:latest
```
# Running
Copy the denonavr.service file to /etc/systemd/system/. Modify the ExecStart path and arguments as necessary.

    systemctl enable denonavr.service  # Enable on boot
    systemctl start denonavr.service   # Start server
    systemctl stop denonavr.service    # Stop server

# Routes
All routes return JSON.

## Power
- GET */power/state* - will return the current power state
- GET */power/turnon* - will turn on the device
- GET */power/turnoff* - will turn off the device
## Volume
- GET */volume/level* - get the current volume level
- GET */volume/set/<int:level_id>* - set the current volume (level_id is in DB)
## Input Source
- GET */input/state* - returns the current input source
- GET */input/switch/<source_id> - will switch to the given source (source one of "dvd", "bd, "game", "satcbl")


inspired by https://github.com/happyleavesaoc/python-firetv

[1]: https://www.denon.de/de/product/hometheater/avreceivers/avrx1000?docname=AVRX1000_E300_PROTOCOL(1000)_V01.pdf

