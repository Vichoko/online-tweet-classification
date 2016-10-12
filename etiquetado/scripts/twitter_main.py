# -*- coding: utf-8 -*-

# PARAM
since = '2015-09-14'
until = '2015-09-18'
query = 'temblor OR tembló OR temblo OR temblar OR temblando OR terremoto OR sismo'


# Programa ejecuta advanced search en Twitter y guarda resultados en output_got.csv
import sys,getopt,got,datetime,codecs
def main():
	tweetCriteria = got.manager.TweetCriteria()	
	tweetCriteria.since = since
	tweetCriteria.until = until
	tweetCriteria.querySearch = query
	
	outputFile = codecs.open("output_got.csv", "w+", "utf-8")
		
	outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
	
	print 'Searching...\n'
	
	def receiveBuffer(tweets):
		lastid = 0
		for t in tweets:
			outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
			lastid = t.id
			lastdate = t.date.strftime("%Y-%m-%d %H:%M")
		outputFile.flush();
		print 'step date %s' % lastdate
		print 'More %d saved on file...\n' % len(tweets)
	
	got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
	
	outputFile.close()
	print 'Done. Output file generated "output_got.csv".'

if __name__ == '__main__':
	main()