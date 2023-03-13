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

> NOTE: Parameters provided by named groups are all in common groups.
>
> NOTE: Dependency injection will not work by default, so you must patch some
> functions to export new functions that support dependency injection if
> needed.

## Loading and using permtab

This step is quite easy:

```python
import permtab

permtab.load("/path/to/your.permtab")  # load "/path/to/your.permtab"

rule = permtab.find_rule("your_rule_name")  # get rule function, then use it

def f():
    if rule(...):
        ...  # run if the condition is satisfied
    else:
        ...  # otherwise
```

## Editing a permtab

Editing uses a `+` and `-` marker on a rule to control changes.

Here is an example:

```python
import permtab

parsed = permtab.parse("test.permtab")
# DO NOT parse and edit the SAME FILE at the same time
# Otherwise your data may be lost

with open("test.permtab", "w") as f:
    f.writelines(
        permtab.edit(
            parsed,
            {
                "myrule1": ("-t_aeiou", "-t_hello world!"),
                # add a `-` to remove an existing rule
                "myrule2": ("+t_hellp",),
                # add a `+` to add a new rule
                "myrule3": ("+t_foo", "+t_bar", "-t_foo")
                # `+` and `-` operation can take effect at the same time
                # duplicate changes will be evaluated
            }
        )
    )

permtab.reset_rule()  # remove rules previously loaded
permtab.load("test.permtab")  # reload new permtab
```
