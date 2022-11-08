poetry install

# Set test ENV
export TN_ENV=~/dev/take-note/tests/test.tn

test_dir=./dirty/test-output/test
dir=$PWD

rm $test_dir -r
mkdir $test_dir

tn "template test" --template new --note "templated note"

cd $dir

# Clean up ENV
unset TN_ENV
