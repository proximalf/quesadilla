poetry install

# Set test ENV
export TN_ENV=~/dev/take-note/tests/test.tn

test_dir=./dirty/test-output/test
dir=$PWD

rm $test_dir -r
mkdir $test_dir

cd $test_dir
echo $PWD
tn -t "global settings" -n "Global config" -vvv
tn --generate-config -vvv
tn -t "generated but not overwritten" -n "Global config" -vvv
echo "SAVE_PATH_NOTES = './'" >> .tn/takenote-config.toml
tn -t "local settings" -n "Local config" -vvv

cd $dir

export TN_ENV=~/dev/take-note/dirty/test-output
cd $TN_ENV
tn --generate-config -vvv
# Clean up ENV
unset TN_ENV

cd $dir
