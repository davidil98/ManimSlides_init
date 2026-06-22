"""Toolkit reutilizable para presentaciones con Manim Slides.

Re-exporta los componentes principales para que se puedan importar
directamente desde `toolkit`:

    from toolkit import SlidesControl, VideoMobject, ManimGraph
"""

from .canvas import (
    SlidesControl,
    TINY_SIZE,
    TITLE_SIZE,
    NORMAL_SIZE,
    HOME,
)
from .video import VideoMobject
from .graphs import ManimGraph

__all__ = [
    "SlidesControl",
    "TINY_SIZE",
    "TITLE_SIZE",
    "NORMAL_SIZE",
    "HOME",
    "VideoMobject",
    "ManimGraph",
]
