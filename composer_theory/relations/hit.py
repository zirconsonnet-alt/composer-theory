from abc import ABC
from typing import Iterable, Union

from ..domain.enums.core import Degrees
from ..domain.enums.harmony import Modes


def _format_degrees(degs: Iterable[Degrees]) -> str:
    return "{" + ", ".join(d.name for d in sorted(degs, key=lambda d: d.value)) + "}"


def _format_role(role: Union[Modes, Degrees]) -> str:
    return getattr(role, "name", str(role))


class ResolveHit(ABC):
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"
