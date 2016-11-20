# -*- coding: utf-8 -*-
import os
import json
import re, string
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
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

clf = MultinomialNB().fit(X_train, y_train)


predicted = clf.predict(X_test)

print(clf.score(X_test, y_test))

