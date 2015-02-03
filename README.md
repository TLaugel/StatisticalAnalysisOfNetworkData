Building a recommender engine respecting privacy for the Netflix Contest
================================

During the Netflix contest, privacy concerns arose as some teams managed to identify the Netflix users in the database although it had been anonymized. This project aims at building a recommender an efficient recommender engine (beating the original goal set by Netflix) while introducing some noise in the covariance to make sure no user can be identified. 

We first compute some movie and user effects, and use them to build the covariance matrix of our graph. Then, we use a SVD decomposition to reduce the noise of our matrix. Finally, we apply a kNN algorithm to get our final recommendations.

This project was made in collaboration with Benjamin DONNOT.

References: 'Differentially Private Recommender Systems:  Building Privacy into the Netflix Prize Contenders', F. McSherry and I. Mironovh (2009)
______________________________________________

This project contains the following files:

Main files:
- DONNOT_Laugel_Project_Proposal.pdf: report of the project, including the mathematical properties checking privacy is ensured and the results of the models
- prep0_extractUntilPeriod.py : collects the movie reviews, gathered in several text files, that were made before a certain date
- prep1_extractTest.py:
- prep2_createCSV.py: gathers the extracted data, still splitted in several text files, in one big csv
- model1_computeEffects.py: first calculations needed to build the covariance matrix
- model2_covarianceMat.py: build the covariance matrix
- model3_SVD.py: Singular Value Decomposition of the covariance matrix (http://en.wikipedia.org/wiki/Singular_value_decomposition) 
- model4_kNN.py: kNN algorithm

Other files:
- res0_countMoviesUsersReviews.py: count number of users and movies
- res1_statDesc.py: compute some properties of our graph
- res2_plotDegDistr.py: degree distribution
