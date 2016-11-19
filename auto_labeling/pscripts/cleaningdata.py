#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Preparar filtro de Stop-Words
from nltk.corpus import stopwords
# Preparar filtro de Stem-Words
from nltk.stem.snowball import SnowballStemmer
# Preparar filtro de caracteres especiales
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

import re

import json

import numpy as np

import unicodedata

with open('class1_tweets.json') as json_data:
    d = json.load(json_data)


finalarray = []

for i in range(0,len(d)):

    finalarray.append(np.array(d[i].items()))

## X es una arreglo con los texto de los tweets
X = []

# y es una arreglo con la clase de si es una alerta en tiempo real o no
y = []

for i in range(0, len(d)):

    X.append(finalarray[i][7][1])
    y.append(int(finalarray[i][5][1]))


try:
    stop = stopwords.words('spanish')
except LookupError as e:
    from nltk import download
    download("stopwords")
    stop = stopwords.words('spanish')

regex = re.compile(ur'[^a-zA-Záéíóú]')

stemmer = SnowballStemmer('spanish')

def process_words(document):
    '''Remueve stop-words, caracteres especiales y stem-words, en ese orden exacto.'''
    word_list = document.split()                                 # Separar documento en una lista de palabras.
    word_list = [word for word in word_list if word not in stop] # Remover stopwords
    word_list = [regex.sub('', word) for word in word_list]      # Remover caracteres especiales
    word_list = [stemmer.stem(word) for word in word_list]       # Remover stemwords (también quita acentos y pasa a lowercase)
    filtered_document = word_list
    return filtered_document

bagofwords = []

for i in range(1,len(X)):
    X[i] = process_words(X[i])
    for j in range(1,len(X[i])):
        bagofwords.append(X[i][j])



cv = CountVectorizer()
X_counts = cv.fit_transform(bagofwords)

# Transforma una matriz de contadores a una version de frecuencias de términos
tf_transformer = TfidfTransformer(use_idf=False).fit(X_counts)
X_tf = tf_transformer.transform(X_counts)

# Al aplicar idf aminoriza el impacto de palabras muy repetidas normalizando las frecuencias
tfidf_transformer = TfidfTransformer()
X_tfidf = tfidf_transformer.fit_transform(X_counts)

print(X_tfidf)
