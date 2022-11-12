poetry install

# Set test ENV
export TN_ENV=~/dev/take-note/tests/test.tn

rm dirty/test-output/*

tn --help > help.output

tn -t "test note" --note "This is a note"

tn --note "This is a note has no title"

tn -t "test - multiline note"

touch "./dirty/test-output/test note"

tn a "TEST" --note "append note"

tn a "test2" --note "append note2"

tn --path "./dirty/test-output" --note "forced path" -t "forced"

# Clean up ENV
unset TN_ENV
