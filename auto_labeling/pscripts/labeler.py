#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import json
from date import Date
import collections

'''
* Jun 2016 0: 2016-06-07 10:51:37 Magnitud: 6.3 Mexico
* Jun 2016 1: 2016-06-10 03:25:22 Magnitud: 6.1 Nicaragua
* Jul 2016 0: 2016-07-11 02:11:04 Magnitud: 6.3 Ecuador
* Jul 2016 1: 2016-07-25 17:26:50 Magnitud: 6.1 Chile
* Ago 2016 0: 2016-08-04 14:15:12 Magnitud: 6.2 Argentina
* Ago 2016 1: 2016-08-18 18:09:43 Magnitud: 6.0 Sur-Este del Oceano Pacifico

DEsde el momento de ocurrido el evento a 4 minutos después pueden etiquetarse como twits de alerta.
Despues de 4 minutos ya hay demasiados twits que no son de alerta

Este programa deja todos los twits de alerta en nuevo json, bota las columnas innecesarias y agrega nueva columna.

Input schema example:
{   "download_date": "2016-08-04T14:32:29",
    "creation_date": "2016-08-04T14:19:20",
    "id_user": 247749446,
    "favorited": 0,
    "lang_tweet": "es",
    "text_tweet": "Empezaron a salir los pokemones de tierra #Antofagasta #temblor",
    "rt": 0,
    "rt_count": 0,
    "has_keyword": 1
    }

Se bota "lang_tweet" y "has_keyword" porque vale "es" y 1 para todos.
Se agrega "class" que vale 1 si es de la clase "alerta" y 0 de lo contrario.

Este script etiqueta Tweets de alerta.

Output schema:
{
    "download_date",
    "creation_date",
    "text_tweet",
    "id_user",
    "favorited",
    "text_tweet",
    "rt",
    "rt_count",
    "class"
}
'''
events = [{'file': "tweetsjun20160", 'event_time': "2016-06-07T10:51:37"},
          {'file': "tweetsjun20161", 'event_time': "2016-06-10T03:25:22"},

          {'file': "tweetsjul20160", 'event_time': "2016-07-11T02:11:04"},
          {'file': "tweetsjul20161", 'event_time': "2016-07-25T17:26:50"},

          {'file': "tweetsago20160", 'event_time': "2016-08-04T14:15:12"},
          {'file': "tweetsago20161", 'event_time': "2016-08-18T18:09:43"},
]


out_attr_list = ["download_date",
    "creation_date",
    "text_tweet",
    "id_user",
    "favorited",
    "text_tweet",
    "rt",
    "rt_count"]

row_array = []

for event in events:
    with open("C:/Users/Vichoko/Documents/GitHub/real-time-twit/auto_labeling/json/tweets_sismos/" + event['file'] + ".json",
              "r") as readfile:
        data = json.load(readfile)  # Lista de diccionarios, cada uno es una fila original

    counter = 0
    for tweet in data:
        # Threshold set to 4 minutes after the event happened to label them as "Alerta en Tiempo Real"
        event_time = Date(event['event_time'])
        limit_date = Date(event['event_time']).sum_minutes(4)
        tweet_date = Date(tweet['creation_date'])

        if tweet_date.compare_to(event_time) < 0:
            # Si el tweet es de antes del evento, lo ignoro
            continue
        elif tweet_date.compare_to(limit_date) <= 0:
            # Si el tweet fue creado antes de la fecha limite y despues del evento, lo guardo
            counter = 0

            d = collections.OrderedDict()
            for attr in out_attr_list:
                d[attr] = tweet[attr]
            d['class'] = 1
            row_array.append(d)

        else:
            # si el twit es de despues de la fehca limite, lo ignoro y pienso en terminar esta tabla
            counter += 1
            if counter > 300:
                # si he visto 300 tweets con fecha mayor a la limite corto el etiquetado (Porque tweets estan ordenados)
                break


j = json.dumps(row_array)
objects_file = "class1_tweets" + ".json"
f = open(objects_file, 'w')
print >> f, j
print("	done")







