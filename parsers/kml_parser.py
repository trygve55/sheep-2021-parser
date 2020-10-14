import sys
import pprint
from pykml import parser
from os import path
from geopy.point import Point

pp = pprint.PrettyPrinter(indent=4)


def parse_kml_file(filename):
    """Parses a kml file into a list of points that can be used with GeoPy."""

    kml_file = path.join(filename)

    points = []

    with open(kml_file) as f:
        doc = parser.parse(f).getroot()
        for e in doc.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
            long, lat, height = e["Point"]["coordinates"].text.split(',')
            points.append(Point(longitude=long, latitude=lat, altitude=str(float(height) / 1000))) # Workaround to make it parse meter as meters instead of km.

    return points


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(
            'Invalid number of arguments.\n\nUsage:\n$ python sheep_parser.py logfile.log')
        exit(1)

    filename = sys.argv[1]

    results = parse_kml_file(filename)

    pp.pprint(results)
