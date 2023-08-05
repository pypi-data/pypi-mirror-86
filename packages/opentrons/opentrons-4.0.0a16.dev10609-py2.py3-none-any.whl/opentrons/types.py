import enum
from math import sqrt, isclose
from typing import Any, NamedTuple, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from typing import (Optional,       # noqa(F401) Used for typechecking
                        Tuple)
    from .protocol_api.labware import (  # noqa(F401) Used for typechecking
        Labware, Well)
    from opentrons.protocols.geometry.module_geometry import ModuleGeometry  # noqa(F401)


class PipetteNotAttachedError(KeyError):
    """ An error raised if a pipette is accessed that is not attached """
    pass


class Point(NamedTuple):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        pairs = ((self.x, other.x), (self.y, other.y), (self.z, other.z))
        return all(isclose(s, o,
                           rel_tol=1e-05, abs_tol=1e-08) for s, o in pairs)

    def __add__(self, other: Any) -> 'Point':
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Any) -> 'Point':
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union[int, float]) -> 'Point':
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Point(self.x*other, self.y*other, self.z*other)

    def __rmul__(self, other: Union[int, float]) -> 'Point':
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Point(self.x*other, self.y*other, self.z*other)

    def __abs__(self) -> 'Point':
        return Point(abs(self.x), abs(self.y), abs(self.z))

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)

    def magnitude_to(self, other: Any) -> float:
        if not isinstance(other, Point):
            return NotImplemented
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        z_diff = self.z - other.z
        return sqrt(x_diff**2 + y_diff**2 + z_diff**2)


LocationLabware = Union['Labware', 'Well', str, 'ModuleGeometry', None]


class Location(NamedTuple):
    """ A location to target as a motion.

    The location contains a :py:class:`.Point` (in
    :ref:`protocol-api-deck-coords`) and possibly an associated
    :py:class:`.Labware` or :py:class:`.Well` instance.

    It should rarely be constructed directly by the user; rather, it is the
    return type of most :py:class:`.Well` accessors like :py:meth:`.Well.top`
    and is passed directly into a method like
    :py:meth:`InstrumentContext.aspirate`.

    .. warning::
       The :py:attr:`labware` attribute of this class is used by the protocol
       API internals to, among other things, determine safe heights to retract
       the instruments to when moving between locations. If constructing an
       instance of this class manually, be sure to either specify `None` as the
       labware (so the robot does its worst case retraction) or specify the
       correct labware for the :py:attr:`point` attribute.


    .. warning::
       The `==` operation compares both the position and associated labware.
       If you only need to compare locations, compare the :py:attr:`point`
       of each item.
    """
    point: Point
    labware: LocationLabware

    def move(self, point: Point) -> 'Location':
        """
        Alter the point stored in the location while preserving the labware.

        This returns a new Location and does not alter the current one. It
        should be used like

        .. code-block:: python

            >>> loc = Location(Point(1, 1, 1), None)
            >>> new_loc = loc.move(Point(1, 1, 1))
            >>> assert loc_2.point == Point(2, 2, 2)  # True
            >>> assert loc.point == Point(1, 1, 1)  # True

        """
        return self._replace(point=self.point + point)


class Mount(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()

    def __str__(self):
        return self.name

    @classmethod
    def string_to_mount(cls, mount: str) -> 'Mount':
        if mount == 'right':
            return cls.RIGHT
        else:
            return cls.LEFT


class TransferTipPolicy(enum.Enum):
    ONCE = enum.auto()
    NEVER = enum.auto()
    ALWAYS = enum.auto()


DeckLocation = Union[int, str]
