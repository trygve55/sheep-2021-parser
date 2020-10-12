from parsers import sheep_parser, kml_parser
from geopy import distance
from math import sqrt


def distance2(point1, point2):
    return sqrt(distance.great_circle((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).m**2 + (point1.altitude - point2.altitude)**2)


if __name__ == '__main__':
    filename_sheep = "logfiles/2020-10-08-clean.log"
    filename_kml = "logfiles/MyLocations_20201008095026.kml"

    samples = sheep_parser.parse_log_file(filename_sheep)
    points = kml_parser.parse_kml_file(filename_kml)

    home_point = points[-1]
    points.remove(home_point)

    samples = samples[1:]

    for i in range(len(points)):
        print(distance2(home_point, points[i]), 'm')
        print(samples[i]['average_distance'])
