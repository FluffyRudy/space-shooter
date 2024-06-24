import pygame, sys
from pathlib import Path
from config import path_dict


def load_image(path_name: str) -> pygame.Surface:
    """
    Load an image from the given relative path's directory name and return it as a pygame Surface.

    Args:
        path_name (str): The relative path's directory name where the image is located.

    Returns:
        pygame.Surface: The loaded image as a pygame Surface object.
    """
    path = path_dict[path_name]
    return pygame.image.load(path).convert_alpha()


def load_frames(path_name: str) -> list[pygame.Surface]:
    """
    Load multiple frames (images) from the given relative path's directory name and return them as a list of pygame Surfaces.

    Args:
        path_name (str): The relative path's directory name where the frames are located.

    Returns:
        list[pygame.Surface]: A list of loaded frames as pygame Surface objects.
    """
    path = path_dict[path_name]
    frames = []

    for file in Path(path).iterdir():
        if file.suffix == ".png":
            surface = load_image(Path(path) / file)
            frames.append(surface)

    return frames
