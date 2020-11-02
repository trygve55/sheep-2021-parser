import sys
import pprint
import serial
from parsers import sheep_parser

pp = pprint.PrettyPrinter(indent=4, depth=1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(
            'Invalid number of arguments.\n\nUsage:\n$ python serial_parser.py serial-port')
        exit(1)

    serial_port = sys.argv[1]

    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = serial_port

    print(ser)
    ser.open()
    print("Started reading from ", serial_port, )

    results = sheep_parser.parse_log(ser, print_input=False)
    #pp.pprint(results)

    ser.close()
