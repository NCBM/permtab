from pathlib import Path
import re
import shlex
from typing import Callable, Dict, Iterable, List, Tuple, TypeVar, Union

_T = TypeVar("_T")


REGISTERED_RULEFACTORY: List[
    Tuple[re.Pattern[str], Callable[..., Callable[..., bool]]]
] = []
_REGISTERED_RULE: Dict[str, Callable[..., bool]] = {"*": lambda: True}
REGISTERED_RULE = dict(_REGISTERED_RULE)


def reset_factory() -> None:
    global REGISTERED_RULEFACTORY
    REGISTERED_RULEFACTORY = []


def reset_rule() -> None:
    global REGISTERED_RULE
    REGISTERED_RULE = dict(_REGISTERED_RULE)


def _defract(fp: Path) -> Iterable[List[str]]:
    with fp.open(encoding="utf-8") as f:
        for ln in f:
            if p := shlex.split(ln, comments=True):
                yield p


def defract(
    fp: Union[str, Path],
    *,
    defract_func: Callable[[Path], Iterable[List[str]]] = _defract
) -> List[List[str]]:
    fp = Path(fp)
    return list(defract_func(fp))


def digest_filter(sfi: str) -> Callable[..., bool]:
    for pat, fac in REGISTERED_RULEFACTORY:
        if (m := pat.match(sfi)) is not None:
            return fac(*m.groups(), **m.groupdict())
    return lambda *args, **kwargs: False


def generate_rule(line: Iterable[str]) -> Tuple[str, Callable[..., bool]]:
    name, *sfilter = line
    ffilter: map[Callable[..., bool]] = map(digest_filter, sfilter)
    def _verify(*args, **kwargs) -> bool:
        return any(filt(*args, **kwargs) for filt in ffilter)
    return name, _verify


def update_rule(name: str, func: Callable[..., bool]) -> None:
    global REGISTERED_RULE
    REGISTERED_RULE.update({name: func})


def load(
    fp: _T,
    *,
    defract_func: Callable[[_T], Iterable[List[str]]] = defract
) -> None:
    for df in defract_func(fp):
        update_rule(*generate_rule(df))