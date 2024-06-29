from random import randint


def random_rgba():
    return tuple([randint(0, 255) for x in range(3)])
