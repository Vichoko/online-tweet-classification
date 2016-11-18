# Resumen

## Obtenci�n de datos
* Se obtuvieron tweets de los meses Junio, Julio y Agosto del a�o 2016 en espa�ol y con palabras claves de sismos en formato en formato SQL.
* Se descargaron datos de sismos con grado 6+ en areas de habla hispana en formato CSV.
* Se descargaron datos de sismos con grado 4+ en todo el mundo en formato CSV.

	
## Etiquetado como 'Alerta en tiempo real'
### Pre-procesamiento de datos
Se exportaron datos de Tweets  de SQL a formato JSON filtrando por: 
	* Con texto en espa�ol
	* Con palabras claves de sismos
	* Con fecha de emision en torno a 1 hora del momento de ocurrencia de un evento sismologico grado 6 o m�s pasado.
	
Se tomaron los tweets emitidos desde el momento del evento sismico hasta 4 minutos despu�s del comienzo del evento y se etiquetaron como 
`class = 1`, es decir, como 'Alerta en Tiempo Real'

## Etiquetado como 'No Alerta en tiempo real' [AUN NO IMPLEMENTADO]
### Pre-procesamiento de datos
Se exportaron datos de Tweets  de SQL a formato JSON filtrando por: 
	* Con texto en espa�ol
	* Con palabras claves de sismos
	* Con fecha de emision lejana a cualquier evento sismico en el mundo de grado 4 o m�s.
	
Se tomaron todos estos tweets y se etiquetaron como `class 2`


