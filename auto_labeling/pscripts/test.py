#!/usr/bin/env python
from __future__ import print_function

import pymysql
import collections

conn = pymysql.connect(host='localhost', user='root', passwd='', db='tweetsjun2016')

cur = conn.cursor()

cur.execute(""" 
			SELECT * FROM 20160607_tweets
			WHERE 20160607_tweets.creation_date >= '2016-06-07 10:51'
			AND 20160607_tweets.creation_date <= '2016-06-07 11:51'
			AND 20160607_tweets.lang_tweet = "es"
			AND 20160607_tweets.has_keyword = 1
			AND 20160607_tweets.rt = 0
			LIMIT 20
			""")

print(cur.description)

print("kakita")

objects_list = []
for row in cur:
	d = collections.OrderedDict()
	d['download_date'] = row.download_date
	d['creation_date'] = row.creation_date
	d['id_user'] = row.id_user
	d['favorited'] = row.favorited
	d['lang_tweet'] = row.lang_tweet
	d['text_tweet'] = row.text_tweet
	d['rt'] = row.rt
	d['rt_count'] = row.rt_count
	d['has_keyword'] = row.has_keyword
	
	objects_list.append(d)
 
j = json.dumps(objects_list)
objects_file = filename + "_dicts"
f = open(objects_file,'w')
print >> f, j

cur.close()
conn.close()