from enum import auto
from ._lookup import LookupEnum

__all__ = ["Textures"]


class Textures(LookupEnum):
    Columnar = "columnar"
    Ascending = "ascending"
    Triangular = "triangular"
    Decomposition = "decomposition"
