# markup - A markup parity

```text
███╗   ███╗ █████╗ ██████╗ ██╗  ██╗██╗   ██╗██████╗
████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██║   ██║██╔══██╗
██╔████╔██║███████║██████╔╝█████╔╝ ██║   ██║██████╔╝
██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██║   ██║██╔═══╝
██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗╚██████╔╝██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝
```

## installation

to install from source run

```text
git clone http://github.com/bob16795/markup
cd markup
python3 setup.py install
```

## usage

Compiles using my parity of markdown markup.

```text
markup [options] file
```

### options

`--help`|`-h`
Show help and exit.

`--verbose`|`-v`
Increases the verbosity, can be used more than once, overrides quiet. default `-vv`

`--fullverbose`|`-V`
Sets verbosity to 1000.

`--quiet`|`-q`
Set verbosity to zero.

`--appendprop`|`-p`
Appends property to the document overriding any property.

`--output`|`-o`
Appends prop to override the output of a document. same as `-p output:`

`--tree`|`-t`
writes the document tree to output (mainly for debug).

`--fileout`
forces the document to output to a file.

`--stdout`
forces the document to output to stdout.

### tricks

to include the text from another document verbatim use `Inc: file`

### doc properties format

`[[!]req [= "req_value"]|] property: value`

- !: reverses the req to be false
- req: the requirement to be req_value
- req_value: the expected value of req
- property: the property to set
- value: the value of the property

### doc property tags

`()tag()`

- tag: the doc prop to include

### doc properties by document type

#### all

- tab_to_spaces: the amount of spaces in a tab defaults to 2
- file_type: the formatter to use for the document
- output_nodule: the module containing the formatter
- output: the file to output to relative to the source code
- ignore: if defined the document is ignored
- use: include a document (can be multiple split by ;) can include path but is relative to the base document

#### special

- slave: true if the file reader is in a `Inc:` statement

#### html

- css_path: the path to a css style sheet

#### pdf_groff

- author: the author of the document
- title: the title of the document
- title_page: if defined will add a title page to the document
- title_head: the level of the first heading

#### pdf_latex & latex

- author: the author of the document
- title: the title of the document
- title_page: if defined will add a title page to the document
- title_head: the level of the first heading
- no_cols: no columns in document
- index: adds an index to the document
- toc: adds a table of contents to the document
- chapter_toc: add a table of contents to each chapter

## <> tags

### format

`<type: text>`

### types by document type

#### pdf_latex & latex

- COL: sets column number in documentIn the column on the left hand side are 10 of the most essential terms for this unit’s content.  In the second column, write the definition on your own words.
- CPT: starts a chapter
- IDX: adds an index entry in current position

## updates

### added tree flag

this does error but still works for debugging

### Decided to use bashbud to generate documentation

first release using a [bashbud](http://github.com/budlabs/bashbud) generated README.

### More options

added more options to the compiler like `--appendprop` and
`--output`.

### Got readme up to date

I finished the readme for now

### A lot has happened

I am nearing a point where i want to add a templating system which will take a while

## known issues

- no tables
- no formating word documents

## license

**markup** is licensed with the **end**
