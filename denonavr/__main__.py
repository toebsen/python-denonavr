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

app = Flask(__name__)


def _is_valid_input_source(source):
    """Only allow special sources.

    :param source: 
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

    :param command: see https://www.denon.de/de/product/homecinema/avreceiver/avrx1200w?docname=Steuerungsprotokoll_IP_RS232C_AVR-X1200W_AVR-X2200W_AVR-X3200W_AVR-X4200W.pdf
    :param config:
    :return:
    """
    try:
        tn = telnetlib.Telnet(config["host"], config["port"], config["timeout"])
    except Exception as e:
        logging.error("Exception occurred: %r" % e)
        return "ERROR"

    try:
        tn.write(("%s\r" % command).encode("ascii"))
        return str(tn.read_until("\r".encode('ascii'))).replace("b'", "").replace("\\r'", "")
    except OSError:
        logging.exception("Exception occurred during writing of telnet")
    finally:
        tn.close()
        return "ERROR"


@app.route('/power/state', methods=['GET'])
def get_power_state():
    """Get current power state.

    :return: current power state PWON/PWStandby
    """
    return jsonify(power=execute("PW?", CONFIG))


@app.route('/power/turnon', methods=['GET'])
def turn_on():
    """Turn on System.

    :return: success
    """
    if execute("PW?", CONFIG) == "PWON":
        return jsonify(power="PWON")
    else:
        return jsonify(power=execute("PWON", CONFIG))


@app.route('/power/turnoff', methods=['GET'])
def turn_off():
    """Turn off System.

    :return: success
    """
    if execute("PW?", CONFIG) == "PWSTANDBY":
        return jsonify(power="PWSTANDBY")
    else:
        return jsonify(power=execute("PWSTANDBY", CONFIG))


@app.route('/input/state', methods=['GET'])
def get_input_state():
    """ Get current Input Source.

    :return: success
    """
    return jsonify(power=execute("SI?", CONFIG))


@app.route('/input/switch/<source_id>', methods=['GET'])
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


@app.route('/volume/level', methods=['GET'])
def get_volume_level():
    """Get the volume level on volume/level.

    :return: Get current volume level
    """
    return jsonify(level=execute("MV?", CONFIG).replace("MV", ""))


@app.route('/volume/set/<int:level_id>', methods=['GET'])
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
    print(CONFIG)
    CONFIG = config["denon"]
    print(CONFIG)


def main():
    """ Set up the server. """
    parser = argparse.ArgumentParser(description='AVR Telnet Server')
    parser.add_argument('-p', '--port', type=int, help='listen port', default=12345)
    parser.add_argument('-c', '--config', type=str, help='config')
    args = parser.parse_args()

    if args.config:
        _read_config(args.config)

    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
