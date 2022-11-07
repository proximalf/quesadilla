poetry install

# Set test ENV
export TN_ENV=~/dev/take-note/tests/test.tn

test_dir=./dirty/test-output/test
dir=$PWD

rm $test_dir -r
mkdir $test_dir

cd $test_dir
echo $PWD
tn --title "global settings" -- "Global config"
tn --generate-config
tn --title "generated but not overwritten" -- "Global config"
echo "SAVE_PATH_NOTES = './'" >> ./.tn/takenote-config.toml
tn  --title "local settings" -- "Local config"

cd $dir

# Clean up ENV
unset TN_ENV
