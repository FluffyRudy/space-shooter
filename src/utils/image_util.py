import pygame, sys
from pathlib import Path


def load_image(path: str, scale_ratio: tuple[float, float] = (1, 1)) -> pygame.Surface:
    """
    Load an image from the given path and return it as a pygame Surface, scaled by the given ratio.

    Args:
        path (str): Path of the image file.
        scale_ratio (tuple[float, float]): Tuple representing the scaling ratio for width and height.

    Returns:
        pygame.Surface: The loaded and scaled image as a pygame Surface object.
    """
    return pygame.transform.scale_by(
        pygame.image.load(path).convert_alpha(), (scale_ratio)
    )


def load_frames(
    path: str, scale_ratio: tuple[int, int] = (1, 1)
) -> dict[str, list[pygame.Surface]]:
    """
    Load multiple frames (images) from subdirectories of the given path and return them as a dictionary of lists of pygame Surfaces.

    Args:
        path (str): Path of the directory containing subdirectories of image files.
        scale_ratio (tuple[int, int]): Tuple representing the scaling ratio for width and height.

    Returns:
        dict[str, list[pygame.Surface]]: A dictionary where keys are subdirectory names and values are lists of loaded and scaled frames as pygame Surface objects.
    """
    frames = {}

    for subdir in sorted(Path(path).iterdir()):
        frame_name = subdir.name
        frames[frame_name] = []
        for file in subdir.iterdir():
            if file.suffix == ".png":
                surface = load_image(Path(path) / file, scale_ratio)
                frames[frame_name].append(surface)

    return frames


def load_frame(
    path: str, scale_ratio: tuple[int, int] = (1, 1)
) -> list[pygame.Surface]:
    """
    Load frames (images) from the given path and return them as a list of pygame Surfaces.

    Args:
        path (str): Path of the directory containing image files.
        scale_ratio (tuple[int, int]): Tuple representing the scaling ratio for width and height.

    Returns:
        list[pygame.Surface]: A list of loaded and scaled frames as pygame Surface objects.
    """
    frames = []

    for file in sorted(Path(path).iterdir()):
        if file.suffix == ".png":
            surface = load_image(Path(path) / file, scale_ratio)
            frames.append(surface)

    return frames
