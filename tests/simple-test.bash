poetry install

# Set test ENV
export TN_ENV=~/dev/take-note/tests/test.tn

rm dirty/test-output/*

tn "test note" --note "This is a note"

tn --note "This is a note has no title"

tn "test - multiline note"

touch "./dirty/test-output/test note"

tn --append "TEST" --note "append note"

tn --append "test2" --note "append note2"

tn --path "./dirty/test-output" --note "forced path" -- "forced"

# Clean up ENV
unset TN_ENV
