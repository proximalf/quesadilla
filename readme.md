# Take-Note!

Very customisable note taking program that is run using the terminal, multiline notes open your favorite editor. As default notes are saved in the directory the program is run, this is a configrable option in `~/.tn/takenote-config.toml`.

```console
tn --help

tn # This opens your favourite editor and saves to choosen directory.

tn "One line note."

tn --title "Quick Note" -- "This is a quick note."

tn --path "./path to save to/"
```

## Configation
There is a global config file, and a local config can be generated with the command `-gc / --generate-config`.

## Templates
[Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) is the templating engine used, its relavtively simple to use and has great integration potential.
Within the config file, there is the section `[TEMPLATES]`, and the keys to templates should be defined here.

`tn -at TEMPLATE` *at stands for apply template - this is nicer to type than tp and t is reserved for title*
`tn --template TEMPLATE`

Example from config
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

Example from config
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
