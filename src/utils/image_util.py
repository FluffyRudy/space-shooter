from typing import Optional
import pygame
from pathlib import Path


def load_image(
    path: str,
    scale_ratio: Optional[tuple[float, float]] = (1.0, 1.0),
    scale_size: Optional[tuple[float, float]] = None,
) -> pygame.Surface:
    """
    Load an image from the given path and return it as a pygame Surface, scaled by the given ratio or size.

    Args:
        path (str): Path of the image file.
        scale_ratio (Optional[tuple[float, float]]): Tuple representing the scaling ratio for width and height. Takes priority over scale_size if provided.
        scale_size (Optional[tuple[float, float]]): Tuple representing the target width and height in pixels. Used if scale_ratio is None.

    Returns:
        pygame.Surface: The loaded and scaled image as a pygame Surface object.
    """
    image = pygame.image.load(path).convert_alpha()
    if scale_ratio:
        return pygame.transform.scale_by(image, scale_ratio)
    elif scale_size:
        return pygame.transform.scale(image, scale_size)
    return image


def load_frames(
    path: str,
    scale_ratio: Optional[tuple[float, float]] = (1.0, 1.0),
    scale_size: Optional[tuple[float, float]] = None,
) -> dict[str, list[pygame.Surface]]:
    """
    Load multiple frames (images) from subdirectories of the given path and return them as a dictionary of lists of pygame Surfaces.

    Args:
        path (str): Path of the directory containing subdirectories of image files.
        scale_ratio (Optional[tuple[float, float]]): Tuple representing the scaling ratio for width and height. Takes priority over scale_size if provided.
        scale_size (Optional[tuple[float, float]]): Tuple representing the target width and height in pixels. Used if scale_ratio is None.

    Returns:
        dict[str, list[pygame.Surface]]: A dictionary where keys are subdirectory names and values are lists of loaded and scaled frames as pygame Surface objects.
    """
    frames = {}

    for subdir in sorted(Path(path).iterdir()):
        frame_name = subdir.name
        frames[frame_name] = []
        for file in subdir.iterdir():
            if file.suffix == ".png":
                surface = load_image(Path(path) / file, scale_ratio, scale_size)
                frames[frame_name].append(surface)

    return frames


def load_frame(
    path: str,
    scale_ratio: Optional[tuple[float, float]] = (1.0, 1.0),
    scale_size: Optional[tuple[float, float]] = None,
) -> list[pygame.Surface]:
    """
    Load frames (images) from the given path and return them as a list of pygame Surfaces.

    Args:
        path (str): Path of the directory containing image files.
        scale_ratio (Optional[tuple[float, float]]): Tuple representing the scaling ratio for width and height. Takes priority over scale_size if provided.
        scale_size (Optional[tuple[float, float]]): Tuple representing the target width and height in pixels. Used if scale_ratio is None.

    Returns:
        list[pygame.Surface]: A list of loaded and scaled frames as pygame Surface objects.
    """
    frames = []

    for file in sorted(Path(path).iterdir()):
        if file.suffix == ".png":
            surface = load_image(Path(path) / file, scale_ratio, scale_size)
            frames.append(surface)

    return frames
