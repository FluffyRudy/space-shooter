from random import randint


def random_rgba():
    return tuple([randint(128, 255) for x in range(3)])
