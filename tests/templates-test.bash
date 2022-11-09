poetry install

# Set test ENV
export TN_ENV=~/dev/take-note/tests/test.tn

test_dir=./dirty/test-output/test
dir=$PWD

rm $test_dir -r
mkdir $test_dir

tn -t "template new test" --template new --note "templated note"
tn -t "template clipboard test" --template link --note "templated note" --clipboard


cd $dir

# Clean up ENV
unset TN_ENV
