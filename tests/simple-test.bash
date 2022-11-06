poetry install

rm dirty/test-output/*

tn --title "test note" -- "This is a note"

tn "This is a note has no title"

tn --title "test - multiline note"

tn --append "TEST" -- "append note"

tn --append "test2" -- "append note2"
