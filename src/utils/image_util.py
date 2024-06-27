import pygame, sys
from pathlib import Path


def load_image(path: str, scale_ratio: tuple[float, float] = (1, 1)) -> pygame.Surface:
    """
    Load an image from the given relative path's directory name and return it as a pygame Surface.

    Args:
        path (str): path of file.

    Returns:
        pygame.Surface: The loaded image as a pygame Surface object.
    """
    return pygame.transform.scale_by(
        pygame.image.load(path).convert_alpha(), (scale_ratio)
    )


def load_frames(
    path: str, scale_ratio: tuple[int, int] = (1, 1)
) -> dict[str, list[pygame.Surface]]:
    """
    Load multiple frames (images) from the given relative path's directory name and return them as a dict of list of pygame Surfaces.

    Args:
        path: path of file.

    Returns:
        dict[str, list[pygame.Surface]]: A list of loaded frames as pygame Surface objects.
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
    Load frames (images) from the given relative path's directory name and return them as a list of pygame Surfaces.

    Args:
        path: path of file.

    Returns:
        list[pygame.Surface]: A list of loaded frames as pygame Surface objects.
    """
    frames = []

    for file in sorted(Path(path).iterdir()):
        if file.suffix == ".png":
            surface = load_image(Path(path) / file, scale_ratio)
            frames.append(surface)

    return frames
