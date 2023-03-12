import permtab
import re


def text_fac(text: str, **kwargs):
    def _filter(intext: str):
        return text == intext
    return _filter

permtab.register_rulefactory(re.compile("t_(.*)"), text_fac)
permtab.load("test.permtab")

assert permtab.find_rule("myrule2")("hellp") == False

with open("edited.permtab", "w") as f:
    f.writelines(
        permtab.edit(
            permtab.parse("test.permtab"),
            {
                "myrule1": ("-t_aeiou", "-t_hello world!"),
                "myrule2": ("+t_hellp",),
                "myrule3": ("+t_foo", "+t_bar", "-t_foo")
            }
        )
    )

permtab.reset_rule()
permtab.load("edited.permtab")

assert permtab.find_rule("myrule1")("aeiou") == False
assert permtab.find_rule("myrule1")("hellp")
assert permtab.find_rule("myrule1")("hello world!") == False
assert permtab.find_rule("myrule2")("hellp")
assert permtab.find_rule("myrule3")("foo") == False
assert permtab.find_rule("myrule3")("bar")