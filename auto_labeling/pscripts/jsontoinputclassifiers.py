import json
import numpy as np

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

print(X[1])
print(y[1])
