# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.cross_validation import KFold
import time
from sklearn.feature_extraction import DictVectorizer
os.chdir('/Users/Seba/R-Proyects/Data Mining CC/Tarea 2')

# Al aplicar idf aminoriza el impacto de palabras muy repetidas normalizando las frecuencias
tfidf_transformer = TfidfTransformer()
X_tfidf = tfidf_transformer.fit_transform(X_counts)

print(X_tfidf)
   
#------------------------------------------
#Dividimos el dataset en train y test, el numero 500 es de referencia
X_train = X_tfidf[:500, :]
X_test = X_tfidf[500:, :]
#Definir el test de train y de test. Para esto hay que cargar el class0_tweets.json
y_train = y[:500]
y_test = y[500:]

svm = SVC()
logistic_regression = LogisticRegression()
#Aqui se le pueden pasar mas clasificadores
classifiers = {
	"Support vector machine": svm,
	"Logistic regression": logistic_regression
}
performances = {}
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