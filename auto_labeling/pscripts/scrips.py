# -*- coding: utf-8 -*-
import os
import json
import re, string
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation
from sklearn.cross_validation import KFold
import time
from sklearn.feature_extraction import DictVectorizer
#----------------------------------------------------------------------

emergency = []
non_emergency = []
#---------------------------------- Leemos datos y almacenamos en arreglos
with open('class1_tweets.json') as data_file:
    data = json.load(data_file)
    for tweet in data:
        text = tweet['text_tweet']
        text_clean = re.sub(r'[^\w]', ' ', text)
        emergency.append(text_clean)

with open('class0_tweets.json') as data_file:
    data = json.load(data_file)
    for tweet in data:
        text = tweet['text_tweet']
        text_clean = re.sub(r'[^\w]', ' ', text)
        non_emergency.append(text_clean)

#---------------------------------------- Intercalamos
text_data = [None] * (len(emergency[:1500]) + len(non_emergency[:1500]))
text_data[0::2] = non_emergency[:1500] #posiciones pares
text_data[1::2] = emergency[:1500] #posiciones impares

#---------------------------------------- Arreglo de etiquetas
y=np.tile([0, 1], 1500)
y_train = y[:2000]
y_test = y[2000:]
#---------------------------------------- TF*IDF
tf_idf_vectorizer = TfidfVectorizer()
X = tf_idf_vectorizer.fit_transform(text_data)
X_train = X[:2000, :]
X_test = X[2000:, :]
#---------------------------------------- Seleccion de clasificadores
svm = SVC()
logistic_regression = LogisticRegression()
SGD = SGDClassifier(loss="hinge", penalty="l2")
gnb = GaussianNB()

classifiers = {
	"Support vector machine": svm,
	"Logistic regression": logistic_regression,
    "Stochastic Gradient Descent": SGD,
}
performances = {}
time_0 = time.time()
n_folds = 10
print ("Evaluating models")
#--------------------------------------Entrenamiento
for name, classifier in classifiers.items():

    performance = []
    fold_indices_generator = KFold(X_train.shape[0], n_folds=n_folds)
    for (train, test) in fold_indices_generator:
        classifier.fit(X_train[train], y_train[train])
        performance.append(classifier.score(X_train[test], y_train[test]))
        performances[name] = np.mean(performance)
    print ("%s: %s" % (name, performances[name]))
time_f = time.time()
print('time')
print(time_f - time_0)

max_performance = max(performances.values())
best_classifier_name = [name for (name, classifier) in classifiers.items() if performances[name] == max_performance][0] #Con esto elegimos el clasificador con la mayor performance
print ("Winner: %s" % best_classifier_name)
print ("Performace on test set: %s" % classifiers[best_classifier_name].score(X_test, y_test))


#------------------------Función para contar TOP 10
def print_top10(vectorizer, clf, class_labels):
    """Prints features with the highest coefficient values, per class"""
    feature_names = vectorizer.get_feature_names()
    for i, class_label in enumerate(class_labels):
        top10 = np.argsort(clf.coef_[0])[-10:]
        print("%s: %s" % (class_label,
              " ".join(feature_names[j] for j in top10)))
