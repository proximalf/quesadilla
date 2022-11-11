# Take-Note!

Very customisable note taking program that operates in the terminal, using your favorite editor.

## Use
*As default notes are saved in the directory the program is run.*

```console
tn --help

tn # This opens your favourite editor and saves to choosen directory.

tn --note/-n "One line note."

tn --title/-t "Quick Note"

tn --path/-p "./path to save to/"
```

### Configation
There is a global config file, and a local config this can be generated with the command. `tn -gc | tn --generate-config`.

Global config: `~/.tn/takenote-config.toml`
Local config: `$PWD/.tn/takenote-config.toml`

### Appending

```console
tn a KEY # Opens editor
```
Append to any notes declared in the config file.
An toml object that uses key as a shortcut for a path of a note to append to.

**Config**
```toml
[APPEND]
long = "./appendthisfile.md"
```


### Templates
[Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) is the templating engine used.
Within the config file, there is the section `[TEMPLATES]`, and the keys to templates should be defined here.

`tn -at TEMPLATE` *at stands for apply template - this is nicer to type than tp and t is reserved for title*
`tn --template TEMPLATE`

**Config**
```toml
[TEMPLATES]
new_note = "new-note.md"
```

Currently only a few keys are supported for templates.
- date : `{{ date.format() }}`
    Inserts date where this placeholder is.
    No default is provided. I like to use: `"%y%m_%d%H%M"`
- title : `{{ title }}`
    Inserts title where this placeholder is.
- note : `{{ note }}`
    Inserts body of note where this placeholder is.

## Title Formatting
Saving a note with out a title is not possible, and so there are two options for title / filename conventions. Within the config file, there is the section `[FORMAT]`, the `short` and `long` title can be defined here.

Just like the templates, [Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) is used here.

**Config**
```toml
[FORMAT]
title={short = "{{ date.format('%y%m_%d%H%M') }}", long = "{{ date.format('%y%m_%d%H%M') }} - {{ title }}"}
```

Currently only two keys are supported:
- date : `{{ date.format() }}`
    Inserts date where this placeholder is.
    No default is provided. I like to use: `"%y%m_%d%H%M"`
- title : `{{ title }}`
    Inserts title where this placeholder is.
