echo "compute the effect (movies/users)"
date "+%Y-%m-%d %H:%M:%S"
./applyScript.sh model1_computeEffects.py sigmas
date "+%Y-%m-%d %H:%M:%S"
echo ""
echo "Compute the covariance Matrices"
./applyScript.sh model2_covarianceMat.py sigmas
date "+%Y-%m-%d %H:%M:%S"
echo "Compute the SVD reduction"
./applyScript.sh model3_SVD.py sigmas
date "+%Y-%m-%d %H:%M:%S"
echo "Compute the kNN"
./applyScript.sh model4_kNN.py sigmas
date "+%Y-%m-%d %H:%M:%S"
