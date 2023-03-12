"""
A simple permission rule parsing library.

Format:

permtab uses a syntax similar to crontab, although it is actually a
reversed version. Actually, the `shlex` is used for parsing.

```
# *.permtab
<rulename> <filter ...>
```

NOTE: Leading a rule to `True` only needs one filter that returns `True`.

Here is an example:

```
myrule1     owner_1234  operator_8525   operator_8390
myrule2     text_hello  text_world      "text_hello world!"
*           user_any
# The tab rule with name '*' is considered a base rule.
# If not defined, the default rule will pass everything to other rules.
```
"""

from .core import (
    parse, load, find_rule, register_rulefactory, reset_factory, reset_rule
)
from .fileedit import update, edit

__all__ = (
    "parse", "load", "find_rule", "reset_factory", "register_rulefactory",
    "reset_rule", "update", "edit"
)