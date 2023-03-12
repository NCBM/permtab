import permtab
import re

def text_fac(text: str, **kwargs):
    def _filter(intext: str):
        return text == intext
    return _filter

permtab.register_rulefactory(re.compile("t_(.*)"), text_fac)
permtab.load("test.permtab")

assert permtab.find_rule("myrule2")("hello world!")
assert permtab.find_rule("myrule2")("hello")
assert permtab.find_rule("myrule2")("hellp") == False
assert permtab.find_rule("myrule2")("world")

assert permtab.find_rule("myrule1")("hello world!")
assert permtab.find_rule("myrule1")("hello") == False
assert permtab.find_rule("myrule1")("hellp")
assert permtab.find_rule("myrule1")("aeiou")