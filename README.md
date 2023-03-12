# permtab

A simple permission rule parsing library.

## Installation

Install permtab via `pip`:

```console
pip install permtab
```

## Format

Permtab uses a syntax similar to crontab, although it is actually a reversed version. Actually, the `shlex` is used for parsing.

```bash
# *.permtab
<rulename> <filter...>
```

Here `filter` has the same meaning with `rule` and `condition`.

> NOTE: Leading a rule to `True` only needs one filter that returns `True`.

Here is an example:

```bash
myrule1     owner_1234  operator_8525   operator_8390
myrule2     text_hello  text_world      "text_hello world!"
*           user_any
# The tab rule with name '*' is considered a base rule.
# If not defined, the default rule will pass everything to other rules.
```

## Rule factory

Rule factory is a function which exports a checker function.

This is a generic definition:

```python
import permtab

def factory(*args, **kwargs):
    def _checker(*args, **kwargs):
        return CONDITION
    return _checker

permtab.register_rulefactory(REGEX_FOR_THE_FACTORY, factory)
```

Exactly, the parameters for rule factory and checker depend on their use.

The parameters for rule factory is decided by groups in provided regex.
All groups that matched are unpacked to positional arguments, and all named
groups that matched are unpacked to keyword arguments.

Checkers' parameters are decided by where the checker called.

> NOTE: parameters provided by named groups are all in common groups.
