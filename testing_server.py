from flask import Flask, request, jsonify
import threading
import serial
from parsers import sheep_parser
import sys
import pprint
from enum import Enum
app = Flask(__name__)


parse_results = []
ser = None
operation_state = {
    "state": "waiting"
}


@app.route('/')
def hello():
    global parse_results
    return pprint.pformat(parse_results, indent=4, depth=2)


@app.route('/state')
def state():
    global operation_state
    return operation_state


@app.route('/command', methods=['Post'])
def command():
    if ser is not None:
        print("Sending command:", request.data)
        ser.writelines(request.data)
        return "OK"
    else:
        return "Not ready"


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid number of arguments.\n\nUsage:\n$ python testing_server.py serial-port')
        exit(1)

    serial_port = sys.argv[1]

    debug = False

    def update_thread():
        global parse_results
        global operation_state
        global ser

        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = serial_port

        print(ser)
        ser.open()
        print("Started reading from \"" + serial_port + "\"")
        sheep_parser.parse_log(ser, print_input=debug, parse_results=parse_results)

    p1 = threading.Thread(target=update_thread, args=())
    p1.start()

    app.run(port=8080, debug=False)  # Debug will not work correctly with threads
