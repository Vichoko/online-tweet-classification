setwd('C:/Users/Vichoko/Documents/GitHub/real-time-twit/etiquetado/r/twits/')

# # read .csv's from folder and asign a df to each
# temp = list.files(pattern="*.csv")
# for (i in 1:length(temp)) assign(temp[i], read.csv(temp[i], sep=';'))

# bind .csv's from folder to single df
temp = list.files(pattern="*.csv")
df <- data.frame()
for (i in 1:length(temp)) df <- rbind(df, read.csv(temp[i], sep=';'))

# delete duplicates
df <- unique(df)

# clean dirty records
vect = c()
for (i in 1:length(df$permalink)){
  if (is.na(df$retweets[i]) || df$retweets[i] == "") vect = c(vect, FALSE)
  else if (is.na(df$favorites[i]) || df$favorites[i] == "") vect = c(vect, FALSE)
  else if (is.na(df$text[i]) || df$text[i] == "") vect = c(vect, FALSE)
  else if (is.na(as.numeric(df$retweets[i]))) vect = c(vect, FALSE)
  else vect = c(vect, TRUE)
}

# cleansed dataFrame
newdf = df[vect,]

# create new column with only the day
newdf['day'] = NA

for (i in 1:length(newdf$date)){# x cada tupla
  newdf$day[i] = as.integer(t(as.data.frame(strsplit( (t(as.data.frame(strsplit(toString(newdf$date[i]),' ')))[1]), '-')))[3])
}

# Histogram of twits per day
hist(newdf$day, main="Histograma de Twits en torno al terremoto del 16-09-2015", xlab="Dias", breaks = 9)


## Cloud of words
# Uncomment these the first time
#Needed <- c("tm", "SnowballC","wordcloud", "NLP")
#install.packages(Needed, dependencies=TRUE)  

library(tm)
library(SnowballC)
library(wordcloud)

query_words = c('http', 'terremoto', 'sismo', 'temblor', 
                'temblar', 'temblando', 'temblo', 'tembló', 'sismo', 'httpwww')
## Make a cloud before the earthquake and after
# before
twtCorpus_b <- Corpus(VectorSource(newdf[newdf$day < 16,]$text))
twtCorpus_b <- tm_map(twtCorpus_b, PlainTextDocument)
twtCorpus_b <- tm_map(twtCorpus_b, removePunctuation)
twtCorpus_b <- tm_map(twtCorpus_b, removeWords, stopwords('spanish'))
twtCorpus_b <- tm_map(twtCorpus_b, removeWords, query_words)

twtCorpus_b <- tm_map(twtCorpus_b, stemDocument)
wordcloud(twtCorpus_b, max.words = 100, random.order = FALSE)

# Make a cloud before the earthquake and after
twtCorpus_a <- Corpus(VectorSource(newdf[newdf$day >= 16,]$text))
twtCorpus_a <- tm_map(twtCorpus_a, PlainTextDocument)
twtCorpus_a <- tm_map(twtCorpus_a, removePunctuation)
twtCorpus_a <- tm_map(twtCorpus_a, removeWords, stopwords('spanish'))
twtCorpus_a <- tm_map(twtCorpus_a, removeWords, query_words)

twtCorpus_a <- tm_map(twtCorpus_a, stemDocument)
wordcloud(twtCorpus_a, max.words = 100, random.order = FALSE)
