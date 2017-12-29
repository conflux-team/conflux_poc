from defs import *
import time


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
