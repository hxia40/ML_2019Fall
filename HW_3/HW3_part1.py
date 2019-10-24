import numpy as np
import pandas as pd
import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import scipy as sp
import time
from sklearn.cluster import KMeans as kmeans
from sklearn.mixture import GaussianMixture as GMM
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split, learning_curve, validation_curve, ShuffleSplit, cross_val_score, cross_validate
# import yellowbrick

if __name__=="__main__":
    # Data Loading & Preprocessing
    scaler = preprocessing.StandardScaler()
    one_hot = preprocessing.OneHotEncoder()

    '''Load and standardize data set MNIST'''
    set1_name = "mnist"

    train = np.genfromtxt('fashion-mnist_train_minor.csv', delimiter=',')[1:, :]
    test = np.genfromtxt('fashion-mnist_test_minor.csv', delimiter=',')[1:, :]

    data1_X_train = train[:, 1:]
    data1_y_train = train[:, 0]
    data1_X_test = test[:, 1:]
    data1_y_test = test[:, 0]

    data1_X_train = scaler.fit_transform(data1_X_train)
    data1_X_test = scaler.transform(data1_X_test)

    data1_y_train = one_hot.fit_transform(data1_y_train.reshape(-1, 1)).todense()
    data1_y_test = one_hot.transform(data1_y_test.reshape(-1, 1)).todense()

    print "set 1 Y train:", data1_y_train

    '''Load and standardize data set ESR'''
    set2_name = "ESR"
    set2 = np.genfromtxt('Epileptic_Seizure_Recognition.csv', delimiter=',', dtype=None)[1:6001, 1:]
    set2 = set2.astype(int)

    data2_X = set2[:, :-1]
    data2_X = scaler.fit_transform(data2_X)
    data2_y = set2[:, -1]
    data2_X_train, data2_X_test, data2_y_train, data2_y_test = train_test_split(data2_X, data2_y, test_size=0.2, random_state=0, stratify=data2_y)

    data2_X_train = scaler.fit_transform(data2_X_train)
    data2_X_test = scaler.transform(data2_X_test)

    data2_y_train = one_hot.fit_transform(data2_y_train.reshape(-1, 1)).todense()
    data2_y_test = one_hot.transform(data2_y_test.reshape(-1, 1)).todense()

    print "set 2 Y train:", data2_y_train

############################## clustering ##############################

    clusters =  [2, 3, 4, 5, 6, 8, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    # clusters =  [2, 20, 200, 1000]
    temp = len(clusters)
    km = kmeans(random_state=5)
    gmm = GMM(random_state=5)

    score_kmean_train_1 = np.zeros(temp)
    score_gmm_train_1 = np.zeros(temp)
    score_kmean_train_2 = np.zeros(temp)
    score_gmm_train_2 = np.zeros(temp)
    score_kmean_test_1 = np.zeros(temp)
    score_gmm_test_1 = np.zeros(temp)
    score_kmean_test_2 = np.zeros(temp)
    score_gmm_test_2 = np.zeros(temp)

    for i in range(0, temp):
        km.set_params(n_clusters = clusters[i])
        gmm.set_params(n_components = clusters[i])

        km.fit(data1_X_train)
        gmm.fit(data1_X_train)
        score_kmean_train_1[i] = km.score(data1_X_train)
        score_gmm_train_1[i] = gmm.score(data1_X_train)
        score_kmean_test_1[i] = km.score(data1_X_test)
        score_gmm_test_1[i] = gmm.score(data1_X_test)

        km.fit(data2_X_train)
        gmm.fit(data2_X_train)
        score_kmean_train_2[i] = km.score(data2_X_train)
        score_gmm_train_2[i] = gmm.score(data2_X_train)
        score_kmean_test_2[i] = km.score(data2_X_test)
        score_gmm_test_2[i] = gmm.score(data2_X_test)

        print i+1

    file_1 = open('file_1.txt','w')

    file_1.write("Cluster")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%i" % clusters[i])
    file_1.write("\n")

    file_1.write("k-mean score train 1")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%1.9f" % score_kmean_train_1[i])
    file_1.write("\n")

    file_1.write("k-mean score test 1")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%1.9f" % score_kmean_test_1[i])
    file_1.write("\n")

    file_1.write("gmm score train 1")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%1.9f" % score_gmm_train_1[i])
    file_1.write("\n")

    file_1.write("gmm score test 1")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%1.9f" % score_gmm_test_1[i])
    file_1.write("\n")

    file_1.write("k-mean score train 2")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%1.9f" % score_kmean_train_2[i])
    file_1.write("\n")

    file_1.write("k-mean score test 2")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%1.9f" % score_kmean_test_2[i])
    file_1.write("\n")

    file_1.write("gmm score train 2")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%1.9f" % score_gmm_train_2[i])
    file_1.write("\n")

    file_1.write("gmm score test 2")
    for i in range(0, temp):
        file_1.write(";")
        file_1.write("%1.9f" % score_gmm_test_2[i])
    file_1.write("\n")

    file_1.close()
   
print "========== END =========="
