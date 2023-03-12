import shlex
from typing import Dict, Iterable, List, Set, Tuple

from permtab.exceptions import BadUpdaterRule


def _apply(base: Set[str], updater: Iterable[str]) -> Set[str]:
    _add, _rem = set(), set()
    for u in updater:
        if not u:
            continue
        op, ru = u[0], u[1:]
        if op == "+":
            _add.add(ru)
        elif op == "-":
            _rem.add(ru)
        else:
            raise BadUpdaterRule(f"rule '{u}' have no symbol '+' or '-'")
    add = _add - _rem
    rem = _rem - _add
    return (base | add) - rem


def update(
    parsed: Iterable[List[str]], data: Dict[str, Iterable[str]]
) -> Iterable[Tuple[str, Set[str]]]:
    data = data.copy()
    for name, *filt in parsed:
        if name in data:
            yield name, _apply(set(filt), data[name])
            del data[name]
        else:
            yield name, set(filt)
    yield from ((name, _apply(set(), data[name])) for name in data)


def edit(
    parsed: Iterable[List[str]], data: Dict[str, Iterable[str]]
) -> Iterable[str]:
    return (
        f"{shlex.join((name, *filt))}\n"
        for name, filt in update(parsed, data)
    )