# Take-Note!

Very customisable note taking program that operates in the terminal, using your favorite editor.

## Use

*As default notes are saved in the directory the program is run.*

`tn -t "Title of a normal note"`
Note will use basic template and an editor will open.

`tn t new`
Basic template note, opens editor.

`tn -t "Title of templated file" t new`
Setting the title of a note that uses the `new` template, refer to config.

### Config

There is a global config file, and a local config this can be generated with the command.

Global config: `tn config -g/--global`
Path: `~/.tn/takenote-config.toml`

Local config: `tn config -l/--local`
Path: `$PWD/.tn/takenote-config.toml`

### Templates

[Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) is the templating engine used.
Within the config file, there is the section `[TEMPLATES]`, and the keys to templates should be defined here.

`tn t TEMPLATE`
`tn t -k/--keys`

**Config**
Currently only a few keys are supported for templates.

- datetime : `{{ datetime.now().strftime("%y%m_%d%H%M") }}`
  Inserts date where this placeholder is.
  No default is provided. I like to use: `"%y%m_%d%H%M"`
- title : `{{ title }}`
  Inserts title where this placeholder is.
- note : `{{ note }}`
  Inserts body of note where this placeholder is.

#### Title Formatting

Saving a note with out a title is not possible, and so there are two options for title / filename conventions. Within the config file, there is the section `[FORMAT]`, the `short` and `long` title can be defined here.

Just like the templates, [Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) is used here.

```toml
[FORMAT.FILENAME]
short = "{{ datetime.now().strftime('%y%m_%d%H%M') }}"
long = "{{ datetime.now().strftime('%y%m_%d%H%M') }} - {{ title }}"
```
