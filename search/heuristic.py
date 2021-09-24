import math


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a, b):
    return math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))


def pow_dist(a, b, _pow=2):
    return pow(a[0] - b[0], _pow) + pow(a[1] - b[1], _pow)
