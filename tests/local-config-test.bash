#tn=~/dev/take-note/takenote
tn=takenote

test_dir=./dirty/test-output/test
dir=$PWD

rm $test_dir -r
mkdir $test_dir

cd $test_dir
echo $PWD
python -m $tn --title "test note2" -- "Global config"
python -m $tn --generate-config
echo "SAVE_PATH_NOTES = './'" > ./tn-config.toml
python -m $tn  --title "test note" -- "Local config"

cd $dir
