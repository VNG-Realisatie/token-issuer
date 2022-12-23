from dataclasses import dataclass
from typing import Any, Type, TypeVar, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class EndPoints:
    brc: str
    nrc: str
    ztc: str
    ac: str
    zrc: str
    drc: str

    @staticmethod
    def from_dict(obj: Any) -> "EndPoints":
        brc = obj["BRC"]
        nrc = obj["NRC"]
        ztc = obj["ZTC"]
        ac = obj["AC"]
        zrc = obj["ZRC"]
        drc = obj["DRC"]
        return EndPoints(brc, nrc, ztc, ac, zrc, drc)

    def to_dict(self) -> dict:
        result: dict = {}
        result["BRC"] = from_str(self.brc)
        result["NRC"] = from_str(self.nrc)
        result["ZTC"] = from_str(self.ztc)
        result["AC"] = from_str(self.ac)
        result["ZRC"] = from_str(self.zrc)
        result["DRC"] = from_str(self.drc)
        return result


def end_points_to_dict(x: EndPoints) -> Any:
    return to_class(EndPoints, x)


def end_points_from_dict(s: Any) -> EndPoints:
    return EndPoints.from_dict(s)
