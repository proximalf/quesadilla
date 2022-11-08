poetry install

# Set test ENV
export TN_ENV=~/dev/take-note/tests/test.tn

test_dir=./dirty/test-output/test
dir=$PWD

rm $test_dir -r
mkdir $test_dir

cd $test_dir
echo $PWD
tn "global settings" -n "Global config"
tn --generate-config
tn "generated but not overwritten" -n "Global config"
echo "SAVE_PATH_NOTES = './'" >> ./.tn/takenote-config.toml
tn "local settings" -n "Local config"

cd $dir

# Clean up ENV
unset TN_ENV
