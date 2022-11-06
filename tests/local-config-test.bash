poetry install

test_dir=./dirty/test-output/test
dir=$PWD

rm $test_dir -r
mkdir $test_dir

cd $test_dir
echo $PWD
tn --title "test note2" -- "Global config"
tn --generate-config
echo "SAVE_PATH_NOTES = './'" >> ./tn-config.toml
tn  --title "test note" -- "Local config"

cd $dir
