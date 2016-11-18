# JSON
Contienen los tweets etiquetados con ```pyscripts/labeler.py```.

## Files
* class1_tweets.json: Tweets etiquetados como 'Alerta en Tiempo Real'
* class0_tweets.json: Tweets etiquetdos como 'No Alerta en Tiempo Real'

## Schema Example
* 	"download_date": "2016-06-07T10:51:57",
*   "creation_date": "2016-06-07T10:51:56",
*   "text_tweet": "Recuerdo un d\u00eda de, *llamada a la 1:45*, \"Micho, me va a dar algo, estoy temblando, me tome un moster y un balium... Que me muero.!!\" Jajaja",
*   "id_user": 547038977,
*   "favorited": 0,
*   "rt": 0,
*   "rt_count": 0,
*   "class": 1

## Unicode capped chars
Caracteres ```\u00x``` se ven asi en el JSON, al importarlos con python se codifican bien.


## Importar con Python
```python
import json

d = {'file': "test2"}

with open("./real-time-twit/auto_labeling/json/tweets_sismos/" + d['file'] + ".json", "r") as readfile:
    data = json.load(readfile)

print(data[0][u'text_tweet'])

# data es una lista de dict
# keys del dict son los del schema pero los strings son unicode, tienen una u antes de las '': u'download_date', u'rt', etc.


```

