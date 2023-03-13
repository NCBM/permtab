from pathlib import Path
from re import Pattern, compile as _compile
import shlex
from typing import Callable, Dict, Iterable, List, Tuple, TypeVar, Union
import warnings

from permtab.exceptions import FilterNotLoaded, IgnoringComments, RuleNotLoaded

_T = TypeVar("_T")


REGISTERED_RULEFACTORY: List[
    Tuple[Pattern[str], Callable[..., Callable[..., bool]]]
] = []
_REGISTERED_RULE: Dict[str, Callable[..., bool]] = {
    "*": lambda *args, **kwargs: True
}
REGISTERED_RULE: Dict[str, Callable[..., bool]] = dict(_REGISTERED_RULE)


def reset_factory() -> None:
    global REGISTERED_RULEFACTORY
    REGISTERED_RULEFACTORY = []


def reset_rule() -> None:
    global REGISTERED_RULE
    REGISTERED_RULE = dict(_REGISTERED_RULE)


def _parse(fp: Path) -> Iterable[List[str]]:
    warnings.warn(
        IgnoringComments(
            "The default parser ignores comments in files, which would "
            "affect editing."
        )
    )
    with open(fp, encoding="utf-8") as f:
        for ln in f:
            if p := shlex.split(ln, comments=True):
                yield p


def parse(
    fp: Union[str, Path],
    *,
    parse_func: Callable[[Path], Iterable[List[str]]] = _parse
) -> List[List[str]]:
    fp = Path(fp)
    return list(parse_func(fp))


def digest_filter(sfi: str) -> Callable[..., bool]:
    for pat, fac in REGISTERED_RULEFACTORY:
        if (m := pat.match(sfi)) is not None:
            return fac(*m.groups(), **m.groupdict())
    warnings.warn(
        FilterNotLoaded(
            f"Filter '{sfi}' does not match any factory, using default "
            "'False' filter."
        )
    )
    return lambda *args, **kwargs: False


def generate_rule(line: Iterable[str]) -> Tuple[str, Callable[..., bool]]:
    name, *sfilter = line
    ffilter: Tuple[Callable[..., bool], ...] = tuple(
        map(digest_filter, set(sfilter))
    )
    # use `set(sfilter)` to remove duplicate filter.

    def _verify(*args, **kwargs) -> bool:
        return any(filt(*args, **kwargs) for filt in ffilter)
    return name, _verify


def update_rule(name: str, func: Callable[..., bool]) -> None:
    global REGISTERED_RULE
    REGISTERED_RULE.update({name: func})


def load(
    fp: _T,
    *,
    parse_func: Callable[[_T], Iterable[List[str]]] = parse
) -> None:
    for df in parse_func(fp):
        update_rule(*generate_rule(df))


def find_rule(name: str = "*") -> Callable[..., bool]:
    if (rule := REGISTERED_RULE.get(name, None)) is not None:
        return rule
    warnings.warn(
        RuleNotLoaded(
            f"Cannot find any rule that matches {name}, using '*' rule "
            "instead."
        )
    )
    return REGISTERED_RULE["*"]


def register_rulefactory(
    pat: Union[str, Pattern[str]], factory: Callable[..., Callable[..., bool]]
) -> None:
    if not isinstance(pat, Pattern):
        pat = _compile(pat)
    REGISTERED_RULEFACTORY.append((pat, factory))