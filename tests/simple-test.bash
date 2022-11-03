# tn=~/dev/take-note/takenote
tn=takenote

rm dirty/test-output/*

python -m $tn --title "test note" -- "This is a note"

python -m $tn "This is a note has no title"

python -m $tn --title "test - multiline note"

python -m $tn --append "TEST" -- "append note"

python -m $tn --append "test2" -- "append note2"
