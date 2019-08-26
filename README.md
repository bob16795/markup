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

`--fileout`  
forces the document to output to a file.

`--stdout`  
forces the document to output to stdout.

---

see `man markup` for more information

## updates

### 08-06-19

**Decided to use bashbud to generate documentation**

first release using a bashbud generated README.
[http://github.com/budlabs/bashbud]

### 08-18-19

**more options**

added more options to the compiler like --appendyaml and
--output.

**got readme up to date**

I finished the readme for now

## known issues

- If you have a tokenized character in a word it requires a preceding backslash.

## license

**markup** is licensed with the **license ^^ license**
