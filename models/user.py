from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

from pydantic import BaseModel

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Authorization:
    component: str
    componentWeergave: str
    scopes: List[str]
    zaaktype: Optional[str] = None
    maxVertrouwelijkheidaanduiding: Optional[str] = None
    informatieobjecttype: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Authorization":
        assert isinstance(obj, dict)
        component = from_str(obj.get("component"))
        component_weergave = from_str(obj.get("componentWeergave"))
        scopes = from_list(from_str, obj.get("scopes"))
        zaaktype = from_union([from_str, from_none], obj.get("zaaktype"))
        max_vertrouwelijkheidaanduiding = from_union(
            [from_str, from_none], obj.get("maxVertrouwelijkheidaanduiding")
        )
        informatieobjecttype = from_union(
            [from_str, from_none], obj.get("informatieobjecttype")
        )
        return Authorization(
            component,
            component_weergave,
            scopes,
            zaaktype,
            max_vertrouwelijkheidaanduiding,
            informatieobjecttype,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["component"] = from_str(self.component)
        result["componentWeergave"] = from_str(self.componentWeergave)
        result["scopes"] = from_list(from_str, self.scopes)
        result["zaaktype"] = from_union([from_str, from_none], self.zaaktype)
        result["maxVertrouwelijkheidaanduiding"] = from_union(
            [from_str, from_none], self.maxVertrouwelijkheidaanduiding
        )
        result["informatieobjecttype"] = from_union(
            [from_str, from_none], self.informatieobjecttype
        )
        return result


class User(BaseModel):
    clientIds: List[str]
    label: str
    heeftAlleAutorisaties: bool
    autorisaties: Optional[List[Authorization]]

    @staticmethod
    def from_dict(obj: Any) -> "User":
        assert isinstance(obj, dict)
        client_ids = from_list(from_str, obj.get("clientIds"))
        label = from_str(obj.get("label"))
        heeft_alle_autorisaties = from_bool(obj.get("heeftAlleAutorisaties"))
        autorisaties = from_list(Authorization.from_dict, obj.get("autorisaties"))
        return User(client_ids, label, heeft_alle_autorisaties, autorisaties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["clientIds"] = from_list(from_str, self.clientIds)
        result["label"] = from_str(self.label)
        result["heeftAlleAutorisaties"] = from_bool(self.heeftAlleAutorisaties)
        result["autorisaties"] = from_list(
            lambda x: to_class(Authorization, x), self.autorisaties
        )
        return result


def user_from_dict(s: Any) -> User:
    return User.from_dict(s)
