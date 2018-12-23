#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module provides state information and some control of an
`Denon AVR X1000` device over a network connection."""

import argparse
import logging
import telnetlib

import yaml
from flask import Flask, jsonify

CONFIG = {
    "host": "192.168.2.25",
    "port": "23",
    "timeout": 5
}

APP = Flask(__name__)

def _is_valid_input_source(source):
    """Only allow special sources.

    :param (str) source: name of source
    :return:
    """
    return source in ["DVD", "BD", "GAME", "SAT/CBL"]


def _convert_input_source(source):
    """Convert input source to proper denon conform name.

    :param source: name of the source
    :return: source name adapted to protocol
    """

    source = source.upper()
    if "SATCBL" in source:
        source = "SAT/CBL"
    return source


def execute(command, config):
    """Execute telnet commands on DENON host.

    :param (str) command: see public protocol
    :param (dict) config: device config

    :return: result from avr telnet connection.
    """
    tn_con = telnetlib.Telnet(config["host"], config["port"], config["timeout"])

    try:
        tn_con.write(("%s\r" % command).encode("ascii"))
        read = str(tn_con.read_until("\r".encode('ascii')))
        read = read.replace("b'", "").replace("\\r'", "")
        return read

    except OSError:
        logging.exception("Exception occurred during writing of telnet")
        return "ERROR"
    finally:
        tn_con.close()

@APP.route('/power/state', methods=['GET'])
def get_power_state():
    """Get current power state.

    :return: current power state PWON/PWStandby
    """
    return jsonify(power=execute("PW?", CONFIG))


@APP.route('/power/turnon', methods=['GET'])
def turn_on():
    """Turn on System.

    :return: success
    """
    if execute("PW?", CONFIG) == "PWON":
        return jsonify(power="PWON")
    return jsonify(power=execute("PWON", CONFIG))


@APP.route('/power/turnoff', methods=['GET'])
def turn_off():
    """Turn off System.

    :return: success
    """
    if execute("PW?", CONFIG) == "PWSTANDBY":
        return jsonify(power="PWSTANDBY")
    return jsonify(power=execute("PWSTANDBY", CONFIG))


@APP.route('/input/state', methods=['GET'])
def get_input_state():
    """ Get current Input Source.

    :return: success
    """
    return jsonify(power=execute("SI?", CONFIG))


@APP.route('/input/switch/<source_id>', methods=['GET'])
def switch_input_source(source_id):
    """Set new Input Source.

    :param source_id:
    :return: success
    """
    success = False
    source = _convert_input_source(source_id)
    current_source = execute("SI?", CONFIG).replace("SI", "")
    print("Requested Source: " + source + " Current SRC: " + current_source)

    if source in current_source:
        print("Not executing src change")
        success = True
    elif not _is_valid_input_source(source):
        success = False
    else:
        execute("SI" + source, CONFIG)
        success = True

    return jsonify(succes=success)


@APP.route('/volume/level', methods=['GET'])
def get_volume_level():
    """Get the volume level on volume/level.

    :return: Get current volume level
    """
    return jsonify(level=execute("MV?", CONFIG).replace("MV", ""))


@APP.route('/volume/set/<int:level_id>', methods=['GET'])
def set_volume_level(level_id):
    """Set Volume level on /volume/set/*.

    :param level_id: db level in the range of 0-60DB
    :return: success
    """
    success = False
    if 0 <= level_id <= 60:
        execute("MV%02d" % level_id, CONFIG)
        success = True
    return jsonify(success=success)


def _read_config(config_file_path):
    """ Parse Config File from yaml file. """
    global CONFIG
    config_file = open(config_file_path, 'r')
    config = yaml.load(config_file)
    config_file.close()
    CONFIG = config["denon"]

def main():
    """ Set up the server."""
    parser = argparse.ArgumentParser(description='AVR Telnet Server')
    parser.add_argument('-p', '--port', type=int,
                        help='listen port', default=5557)
    parser.add_argument('-c', '--config', type=str, help='config')
    args = parser.parse_args()

    if args.config:
        _read_config(args.config)

    APP.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
