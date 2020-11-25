import sys
import re
import pprint

pp = pprint.PrettyPrinter(indent=4, depth=1)


def rtt_distance_meters(ticks):
    """Calculates the distance the signal traveled by using Round-Trip delay Time given in ticks."""

    return max(0.0, (299.792458 * (ticks / 16.0) / 2.0))


def read_line(ser, print_input=False):
    line = str(ser.readline())
    if print_input:
        print(line)
    return line


def parse_log_file(filename):
    file = open(filename, 'r')
    return parse_log(file)


def parse_log(file, print_input=False, parse_results=[], operation_state={}):
    """Parses a terminal output logfile from the sheep-2021 project and returns a list containing all measurements."""

    line = " "

    while line != "":
        line = read_line(file, print_input=print_input)
        operation_state["state"] = "idle"
        operation_state["receivedRtt"] = 0
        operation_state["device"] = "NA"

        if "Scanning... [Round" not in line:
            continue

        operation_state["state"] = "scanning"

        scan_label = line.split('[', 1)[1].split(']')[0]

        line = read_line(file, print_input=print_input)
        if "Found" not in line:
            continue
        device_mac = str(re.search('([0-9A-Fa-f]{2}:?){6}', line)[0])
        operation_state["state"] = "found"
        operation_state["device"] = device_mac

        line = read_line(file, print_input=print_input)
        if "Connected" not in line:
            continue
        operation_state["state"] = "connected"

        rtt_samples = []
        line = read_line(file, print_input=print_input)
        while "RTT ticks" in line:
            rtt_samples.append({
                "rttTicks": int(re.search('\s\-?\d+\s', line)[0].strip()),
                "distance": float(re.search('\s\d+.\d+\s', line)[0].strip()),
                "rssi": int(re.findall('\s\-?\d+\s', line)[1].strip())
            })

            operation_state["receivedRtt"] += 1

            line = read_line(file, print_input=print_input)

        if "packets received" not in line:
            continue

        received_packets = int(re.findall('\s\d+\s', line)[0].strip())
        total_packets = int(re.findall('\s\d+\s', line)[1].strip())
        packet_loss = 1 - received_packets / total_packets
        line = read_line(file, print_input=print_input)
        average_distance = float(re.search('\s\d+.\d+\s', line)[0].strip())
        line = read_line(file, print_input=print_input)
        minimum_distance = float(re.search('\s\d+.\d+\s', line)[0].strip())

        average_rssi = sum([i['rssi'] for i in rtt_samples]) / len(rtt_samples)

        parse_results.append({
            'label': scan_label,
            'rttSamples': rtt_samples,
            'average_distance': average_distance,
            'minimum_distance': minimum_distance,
            'received_packets': received_packets,
            'total_packets': total_packets,
            'packet_loss': packet_loss,
            'average_rssi': average_rssi,
            'device_mac': device_mac
        })

    return parse_results


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(
            'Invalid number of arguments.\n\nUsage:\n$ python sheep_parser.py logfile.log')
        exit(1)

    filename = sys.argv[1]

    results = parse_log_file(filename)
    pp.pprint(results)
