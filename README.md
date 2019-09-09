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
markup --help|-h
markup --verbose|-v
markup --fullverbose|-V
markup --appendyaml|-y
markup --output|-o
markup --tree|-t
markup --fileout
markup --stdout
```

`--help`|`-h`  
Show help and exit.

`--verbose`|`-v`  
Increases the verbosity, can be used more than once.

`--fullverbose`|`-V`  
Sets verbosity to 1000.

`--appendyaml`|`-y`  
Appends yaml to the document overriding any tag.

`--output`|`-o`  
Appends yaml to override the output of a document.

`--tree`|`-t`  
writes the document tree to output (mainly for debug).

`--fileout`  
forces the document to output to a file.

`--stdout`  
forces the document to output to stdout.

---

see `man markup` for more information

### tricks

to include the text from another document verbatim use Inc: then define the document to include

### yaml

#### prefixes

s | : if compiling a used document
m | : if compiling a master document

#### all

file_type: the formatter to use for the document
output_nodule: the module containing the formatter
output: the file to output to relative to the source code
ignore: if defined the document is ignored
use: include a document (can be multiple split by ;)

#### pdf_groff

author: the author of the document
title: the title of the document
title_page: if defined will add a title page to the document
title_head: the level of the first heading

## updates

### added tree flag

this does error but still works for debugging

### Decided to use bashbud to generate documentation

first release using a [bashbud](http://github.com/budlabs/bashbud) generated README.

### more options

added more options to the compiler like --appendyaml and
--output.

### got readme up to date

I finished the readme for now

## known issues

- no tables
- no formating word documents

## license

**markup** is licensed with the **license ^^ license**
