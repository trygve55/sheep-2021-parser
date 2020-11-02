import sys
import re
import pprint

pp = pprint.PrettyPrinter(indent=4, depth=1)


def rtt_distance_meters(ticks):
    """Calculates the distance the signal traveled by using Round-Trip delay Time given in ticks."""

    return max(0.0, (299.792458 * (ticks / 16.0) / 2.0))


def random_n_samples(samples, n, seed=None):
    pass


def read_line(ser, print_input=False):
    line = str(ser.readline())
    if print_input:
        print(line)
    return line


def parse_log_file(filename):
    file = open(filename, 'r')
    return parse_log(file)


def parse_log(file, print_input=False):
    """Parses a terminal output logfile from the sheep-2021 project and returns a list containing all measurements."""

    parse_results = []

    line = " "

    while line != "":
        line = read_line(file, print_input=print_input)

        if "Scanning... [Round" not in line:
            continue

        scan_label = line.split('[', 1)[1].split(']')[0]

        line = read_line(file, print_input=print_input)
        line = read_line(file, print_input=print_input)
        line = read_line(file, print_input=print_input)

        rtt_samples = []

        while "RTT ticks" in line:
            rtt_samples.append({
                "rttTicks": int(re.search('\s\-?\d+\s', line)[0].strip()),
                "distance": float(re.search('\s\d+.\d+\s', line)[0].strip()),
                "rssi": int(re.findall('\s\-?\d+\s', line)[1].strip())
            })

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
            'average_rssi': average_rssi
        })

        pp.pprint(parse_results[-1])

    return parse_results


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(
            'Invalid number of arguments.\n\nUsage:\n$ python sheep_parser.py logfile.log')
        exit(1)

    filename = sys.argv[1]

    results = parse_log_file(filename)
    pp.pprint(results)

    random_n_samples(results, 100)
