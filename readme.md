# Take-Note!


## Templates
[Jinja]() is the templating engine used, its relavtively simple to use and has great integration potential.

`tn -at TEMPLATE` *at stands for apply template - this is nicer to type than tp and t is reserved for title*
`tn --template TEMPLATE`

Currently only a few keys are supported for templates.
- date : `{{ date.format() }}`
    Inserts date where this placeholder is.
    No default is provided. I like to use: `"%y%m_%d%H%M"`
- title : `{{  title }}`
    Inserts title where this placeholder is.
- note : `{{ note }}`
    Inserts body of note where this placeholder is.
