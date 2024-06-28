import math


def calculate_center(size: tuple[int, int], referance_size: tuple[int, int] = (0, 0)):
    return (size[0] - referance_size[0]) // 2, (size[1] - referance_size[1]) // 2
