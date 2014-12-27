echo "start extraction"
date "+%Y-%m-%d %H:%M:%S"
./extractMany.sh dates-extract
echo ""
echo "create csv"
date "+%Y-%m-%d %H:%M:%S"
./applyScript.sh CreateCSV.py dates-extract2
echo ""
echo "compute the effect (movies/users)"
date "+%Y-%m-%d %H:%M:%S"
./applyScript.sh model1_computeEffects.py dates-extract2
date "+%Y-%m-%d %H:%M:%S"
