"""
A simple permission rule parsing library.

Format:
    permtab uses a syntax similar to crontab, although it is actually a
    reversed version.

```
    # *.permtab
    <rulename> <filter ...>
```

    > NOTE: If any filter is determined successfully, the rule can be
    > tendable.

    Here is an example:

```
    myrule1     owner_1234  operator_8525   operator_8390
    myrule2     text_hello  text_world      "text_hello world!"
    *           user_any
    # The tab rule with name '*' is considered a base rule.
    # If not defined, the default rule will pass everything to other rules.
```
"""

from .core import load, reset_factory, reset_rule

__all__ = ("load", "reset_factory", "reset_rule")