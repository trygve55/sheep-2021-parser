import sys
import re
import pprint

pp = pprint.PrettyPrinter(indent=4, depth=2)


def rtt_distance_meters(ticks):
    max(0.0, (299.792458 * (ticks / 16.0) / 2.0))


def random_n_samples(samples, n, seed=None):
    pass


def parse_log_file(filename):

    parse_results = []

    file = open(filename, 'r')
    lines = file.readlines()

    for line_index in range(len(lines)):
        if "Scanning... [Round" not in lines[line_index]:
            continue

        line_index += 3

        rtt_samples = []

        while line_index < len(lines) and "RTT ticks" in lines[line_index]:
            rtt_samples.append({
                "rttTicks": int(re.search('\s\-?\d+\s', lines[line_index])[0].strip()),
                "distance": float(re.search('\s\d+.\d+\s', lines[line_index])[0].strip()),
                "rssi": int(re.findall('\s\-?\d+\s', lines[line_index])[1].strip())
            })

            line_index += 1

        if line_index >= len(lines):
            continue

        received_packets = int(re.findall('\s\d+\s', lines[line_index])[0].strip())
        total_packets = int(re.findall('\s\d+\s', lines[line_index])[1].strip())
        packet_loss = 1 - received_packets / total_packets
        line_index += 1
        average_distance = float(re.search('\s\d+.\d+\s', lines[line_index])[0].strip())
        line_index += 1
        minimum_distance = float(re.search('\s\d+.\d+\s', lines[line_index])[0].strip())

        average_rssi = sum([i['rssi'] for i in rtt_samples]) / len(rtt_samples)

        parse_results.append({
            'rttSamples': rtt_samples,
            'average_distance': average_distance,
            'minimum_distance': minimum_distance,
            'received_packets': received_packets,
            'total_packets': total_packets,
            'packet_loss': packet_loss,
            'average_rssi': average_rssi
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

    random_n_samples(results, 100)
