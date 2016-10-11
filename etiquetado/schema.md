# Schema twit:
	```username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink```
	
	## Ejemplo:
		```LuisRobledoo;2014-04-02 20:59;0;1;"Y al final el profe Uribe tuvo razon sobre el terremoto de Chile. Yo a Uribe lo sigo hasta la muerte (? Jajaja";;;;"451509375791017984";https://twitter.com/LuisRobledoo/status/451509375791017984```

	## Atributos relevantes:
		* date: formato yyyy-mm-dd hh:mm
		* retweets: int
		* text: str
		* favorites: int
		
	## Atributos descartados:
		* geo: la poca cantidad de twits geolocalizados hace dificil utilizar este atributo
		* id
		* permalink
		* username
		
		

# Schema sismologia:
	```time,latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,net,id,updated,place,type,horizontalError,depthError,magError,magNst,status,locationSource,magSource```

	## Ejemplo:
		```2010-02-27T06:34:11.530Z,-36.122,-72.898,22.9,8.8,mwc,454,17.8,,1.09,us,usp000h7rf,2016-05-03T15:30:47.329Z,"offshore Bio-Bio, Chile",earthquake,,9.2,,,reviewed,us,us```

	## Atributos relevantes:
		* time: yyyy-mm-dd'T'hh:mm:ss.sss'Z'
		* mag: Float, Righter
		* depth: Float, Kms
		* place: str
	
	## Atributos descartados:
		* magType
		* nst
		* gap 
		* dmin 
		* rmd 
		* net 
		* id 
		* updated
		* type
		* hortizontalError,
		* depthError
		* magError
		* magNst
		* status
		* locationSource
		* magSource