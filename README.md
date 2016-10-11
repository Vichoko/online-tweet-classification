# real-time-twit
Real time alert classificator for Twits 

# Introduccion
En el problema de detectar a tiempo eventos a través de Twitter surge la dificultad de diferenciar Twits que hablan realmente de una alerta
de otros que, si bien mencionan palabras claves que pueden caracterizar un evento, no son twits que hablan de una alerta en tiempo real.

# Desarrollo
Para este proyecto se abordará la detección de Eventos Sismologicos en Chile. Y de tener buenos resultados se podrá extender este repositorio.

Para construir el clasificador se evaluará la efectividad de distintos algoritmos de clasificación.


# Particularidades

## 1. Obtencion de datos etiquetados
Para conseguir los datos de entrenamiento (y de prueba) se etiquetaran los datos cruzando la base de datos de eventos sismologicos del *Centro Sismologico Nacional*
con 'twits' extraídos de distintas fechas. 

Limitandonos a datos geologicos cercanos a Chile, tecnicamente del area que comprende :: ```Latitud -16 a -57, longitud -112 a -66```

Se extraeran twits que contienen palabras claves ('keywords') que permiten identificar un evento sismologico en Chile como: 
```'temblor', 'tembló', 'temblo', temblar', 'temblando', 'terremoto', 'sismo', '```

Los Twits emitidos durante el día de un evento se etiquetan como "Alerta en tiempo real", los emitidos durante días sin eventos serán etiquetados como 
"No alerta en tiempo real".

Se evaluará hacer un proceso posterior de limpieza de datos para asegurar un buen entrenamiento de los clasificadores.

## 2. Entrenamiento de clasificadores

