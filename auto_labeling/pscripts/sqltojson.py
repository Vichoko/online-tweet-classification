import pyodbc
import json
import collections

class sql_to_json:
	def __init__(self, servername, dbname):
		#constr = 'DRIVER={MySQL};SERVER=' + servername + ";DATABASE=" + dbname + ';'
		constr = "DRIVER={MySQL ODBC 5.3 Unicode Driver};Login Prompt=False;UID=root;Password=;Data Source="+servername+";Database="+dbname
		conn = pyodbc.connect(constr)
		self.cursor = conn.cursor()
	
	def query_tweets(self, query, filename, enable_row_array = 0, enable_k_v = 1):
		self.cursor.execute(query)
		rows = self.cursor.fetchall()

		if enable_row_array:
			# Convert query to row arrays
			rowarray_list = []
			for row in rows:
				t = (row.download_date, row.creation_date, row.id_user, row.favorited, 
					 row.lang_tweet, row.text_tweet, row.rt, row.rt_count, row.has_keyword)
				rowarray_list.append(t)
			 
			j = json.dumps(rowarray_list)
			rowarrays_file = filename + "_rows"
			f = open(rowarrays_file,'w')
			print >> f, j
			
		if enable_k_v:
		# Convert query to objects of key-value pairs
			objects_list = []
			for row in rows:
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
			 
			conn.close()
		
		
if __name__=="__main__":
	a = sql_to_json("localhost", "tweetsjun2016")
	query = """ 
			SELECT * FROM 20160607_tweets
			WHERE 20160607_tweets.creation_date >= '2016-06-07 10:51'
			AND 20160607_tweets.creation_date <= '2016-06-07 11:51'
			AND 20160607_tweets.lang_tweet = "es"
			AND 20160607_tweets.has_keyword = 1
			AND 20160607_tweets.rt = 0
			"""
	a.query_tweets(query, "test")