#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pymysql
import collections
import json

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

#print(cur.description)

print("kakita")

objects_list = []
for row in cur:
	d = collections.OrderedDict()
	d['download_date'] = row[1]
	d['creation_date'] = row[2]
	d['id_user'] = row[5]
	d['favorited'] = row[7]
	d['lang_tweet'] = row[10]
	d['text_tweet'] = row[11].decode('latin1')
	d['rt'] = row[12]
	d['rt_count'] = row[13]
	d['has_keyword'] = row[19]
	
	objects_list.append(d)
	print(row[11].decode('latin1'))
	
	
def date_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError


j = json.dumps(objects_list, default=date_handler, encoding='latin1')
objects_file = "test23" + "_dicts"
f = open(objects_file,'w')
print >> f, j

cur.close()
conn.close()