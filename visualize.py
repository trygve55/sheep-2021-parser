from parsers import sheep_parser, kml_parser
from geopy import distance
from math import sqrt
import sys


def distance2(point1, point2):
    """Calculates the distance between two points by latitude, longitude and altitude. Innaccurate over very long distances."""

    return sqrt(distance.great_circle((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).m**2 + (point1.altitude - point2.altitude)**2)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Invalid number of arguments.\n\nUsage:\n$ python sheep_parser.py logfile.log locations.kml')
        exit(1)

    filename_sheep = sys.argv[1] # Can use '2020-10-08-clean.log' as an example
    filename_kml = sys.argv[2] # Can use 'MyLocations_20201008095026.kml' as an example

    # Start loading of files
    measurements = sheep_parser.parse_log_file(filename_sheep)
    points = kml_parser.parse_kml_file(filename_kml)
    # Ending loading of files

    # Create a list of samples containing the measurements and the points they go between. Modify here.
    home_point = points[-1]
    points.remove(home_point)
    measurements = measurements[1:]

    samples = []

    if len(measurements) != len(points):
        raise Exception("Measurements and points list have different length")

    for i in range(len(measurements)):
        samples.append({
            "measurement": measurements[i],
            "point_from": home_point,
            "point_to": points[i]
        })

    # Calculate and print the distance between home_point and other points
    for s in samples:
        print(distance2(s["point_from"], s["point_to"]), 'm')
        print(s["measurement"]['average_distance'])
