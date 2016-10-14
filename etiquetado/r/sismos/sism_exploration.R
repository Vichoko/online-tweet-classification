setwd('C:/Users/Vichoko/Documents/GitHub/real-time-twit/etiquetado/r')
sismos <- read.csv('sism.csv')

# Para cachar
sismos6 <- sismos[sismos$mag > 6,]


hist(sismos$mag, main="Histograma de magnitudes de 6 a 9", xlab = "Magnitudes", 
     xlim = c(6,9), ylim = c(0,110), breaks=4)
hist(sismos$mag, breaks=5, main="Histograma de magnitudes de 5 a 9", xlab = "Magnitudes")

# Este es el q mas me gusta
hist(sismos$mag, main="Histograma de magnitudes 6 a 9", xlab = "Magnitudes", 
     xlim = c(6,9), ylim = c(0,100), breaks=7)

##
# Agregar nueva columa con años
sismos["year"]=NA

for (i in 1:length(sismos$time)){# x cada tupla
  sismos$year[i] = as.integer(t(as.data.frame(strsplit(
          t(as.data.frame(strsplit(toString(sismos$time[i]),'T')))[1], '-'))))[1]
}

# Cantidad de terremotos por año 
hist(sismos[sismos$mag >= 6,]$year, main="Histograma de terremotos >= 6, por año",
     xlab="Años", xlim=c(2006, 2017), breaks=11)

