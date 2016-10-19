from ..models.Command0Arg import Command0Arg


TEXT = """You can format the message using HTTP GET parameters after your publish URL:

*title*
Accept ONE value, in one of the formats below.
\u2022 `SomeString` - Title will always be "SomaString"
\u2022 `{some_key}` - Title will be the value of the key "some\_key". If "some\_key" doesn't exist, then title will not be sown
\u2022 `{some_key:DefaultStr}` - Title will be the value of the key "some\_key". If "some\_key" doesn't exist, then title will be "DefaultStr"

*keys:*
Accept a comma separated list of values, in one of the formats below (you can mix formats).
\u2022 `some_key` - Will print "*some_key*: value of some\_key". If "some\_key" doesn't exist, then this item will not be sown
\u2022 `some_key:Label` - Will print "*Label*: value of some\_key". If "some\_key" doesn't exist, then this item will not be sown
\u2022 `some_key:Label:DefaultStr` - Will print "*Label*: value of some\_key" if "some\_key" exists, and print "*Label*: DefaultStr" if not
\u2022 `::` - Gives a blank line, just to visual separation

You can access deeper levels from your JSON objects and lists using dot-notation.
If your key have a dot, you can escape that with "\\."
Suppose your publish is is this format:
```
{
  "foo": "FOO",
  "bar": "BAR",
  "baz": 0,
  "list": [{"aa": "AA"},{"bb": "BB"}],
  "have.dot": "HAVE.DOT",
  "obj": {
    "qq": "QQ",
    "ww": "WW"
  }
}
```
and your publish URL looks like this:
```
http://localhost/publish/abC1De_2Fgh3ijKl45MnoPQ6/?title=Test&keys=have\.dot,obj.qq:My qq,::,list.1.bb:List Item,baz:BAZ,default:Default:String Default
```
then you will have a message like:
----------------
*Test*

*have.dot:* HAVE.DOT
*My qq:* QQ

*List Item:* BB
*BAZ:* 0
*Default:* String Default
----------------
"""


class DocsCmd(Command0Arg):
    cmd = '/docs'

    def without_argument(self):
        return TEXT
