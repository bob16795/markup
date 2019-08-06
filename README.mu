---
file_type: html
---
# markup

## creating documents

### escape chars

there are currently isues with the following characters which requires you to use a backslash before them.

* \_
* \`
* \*
* \+
* \-
* \#
* \<
* \>
* \[
* \)

## developing decorators

### Formatter

the formatter decorator can be used to create a formatter for a document.

```

@Formatter
class formatter\_name(\):
  def outer\_init(self, out, info\):
    """
    This function should construct the output classes varables for adding text.
    out: is the return from the function start
    info: it the yaml from  the document
    self.out: the value used for internal output storage.
    """
  def outer\_add(self, out\):
    """ returns self 
    This function should add text to the internal output storage.
    out: the value to add tho the internal output storage
    """
  def fmt\_init(self, \*\*options\):
    """
    This is the init function for the pygments formatter class.
    This is better documented at http://pygments.org/docs/formatterdevelopment/.
    """
  def fmt\_format(self, tokensource, outfile\):
    """
    this is the Format function for the pygments formatter class.
    This is better documented at http://pygments.org/docs/formatterdevelopment/.
    outfile: the outter class
    """
  def add\_new\_line(\):
    """returns var to be used in outter\_add(\)
    this adds a new line
    """
  def add\_text(text\):
    """returns var to be used in outter\_add(\)
    this adds text, should make sure that text.strip(" "\) != ""
    text: the text to add 
    """
  def emph\_text(text\):
    """returns var to be used in outter\_add(\)
    text: the text to add
    """
```
