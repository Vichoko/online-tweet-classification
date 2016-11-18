#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import json
import collections
import datetime
import inspect_sismos
import date


class sql_to_json:
    def __init__(self, address, user, pw):
        self.address = address
        self.user = user
        self.pw = pw
        self.db = None
        self.conn = None
        self.cursor = None

    def connect_db(self, dbname):
        print("conectan2 to " + dbname + "...")
        self.conn = pymysql.connect(host=self.address, user=self.user, passwd=self.pw, db=dbname, charset='utf8mb4')
        print("	done")
        self.cursor = self.conn.cursor()

    def query_tweets(self, query, filename, enable_row_array=0, enable_k_v=1, verbose=0):
        print("Executing query...")
        if verbose:
            print("Query: " + query)
            print("Filename: " + filename)
        self.cursor.execute(query)
        print(" done")

        if False:
            # @NON-FUNCTIONAL
            # Convert query to row arrays
            rowarray_list = []
            for row in self.cursor:
                t = (row.download_date, row.creation_date, row.id_user, row.favorited,
                     row.lang_tweet, row.text_tweet, row.rt, row.rt_count, row.has_keyword)
                rowarray_list.append(t)

            j = json.dumps(rowarray_list)
            rowarrays_file = filename + "_rows"
            f = open(rowarrays_file, 'w')
            print >> f, j

        if enable_k_v:
            print("exporting to JSON...")
            objects_list = []

            for row in self.cursor:
                d = collections.OrderedDict()
                # Atributos escogidos
                d['download_date'] = row[1]
                d['creation_date'] = row[2]
                d['id_user'] = row[5]
                d['favorited'] = row[7]
                d['lang_tweet'] = row[10]
                d['text_tweet'] = row[11]
                d['rt'] = row[12]
                d['rt_count'] = row[13]
                d['has_keyword'] = row[19]

                objects_list.append(d)
            # print(row[11].decode('latin1')) <- Se ven bien con este encoding

            print("got list of dict")
            print("building outfile...")

            def date_handler(obj):
                # Esto es para que las fechas no tiren error
                if hasattr(obj, 'isoformat'):
                    return obj.isoformat()
                else:
                    raise TypeError

            j = json.dumps(objects_list, default=date_handler)
            objects_file = filename + ".json"
            f = open(objects_file, 'w')
            print >> f, j
            print("	done")

    def mult_query_tweets(self, dbname, queries):
        self.connect_db(dbname)
        print("starting multiple queries")
        for i in range(len(queries)):
            query = queries[i]
            self.query_tweets(query, filename=dbname + str(i))

        self.close()
        return

    def close(self):
        self.cursor.close()
        self.conn.close()
        return


databases = [{'name': "tweetsjun2016", 'month': 6, 'year': 2016},
             {'name': "tweetsjul2016", 'month': 7, 'year': 2016},
             {'name': "tweetsago2016", 'month': 8, 'year': 2016}]


def build_db_n_query_for_sismic_spanish_non_rt_tweets(start_time, end_time, verbose=0):
    ''' Recibe s_t y e_t del tipo Date o timedate (ambos tienen mismos attr).
    Genera query para ella.
    '''
    assert start_time.month == end_time.month
    assert start_time.year == end_time.year
    if start_time.day != end_time.day:
        print(
        "build_query_for_sismic_spanish_non_rt_tweets :: Los tiempos que se pasaron corresponden a 2 dias distintos.")
        return ""

    month = date.attr_to_string(start_time.month)
    year = date.attr_to_string(start_time.year)
    day = date.attr_to_string(start_time.day)

    dbname = None
    for db in databases:
        if db['month'] == start_time.month:
            dbname = db['name']

    table_name = year + month + day + '_tweets'
    start_time_formatted = year + '-' + month + '-' + day + ' ' + date.attr_to_string(start_time.hour) + ':' + date.attr_to_string(start_time.minute)
    end_time_formatted = year + '-' + month + '-' + day + ' ' + date.attr_to_string(end_time.hour) + ':' + date.attr_to_string(end_time.minute)

    if verbose:
        print ("Start Time Formatted: " + start_time_formatted + "Start Time: " + str(start_time))
        print ("End Time Formatted: " + end_time_formatted + "End Time: " + str(end_time))
    query = """
        SELECT * FROM """ + table_name + """
        WHERE """ + table_name + """.creation_date >= '""" + start_time_formatted + """'
        AND """ + table_name + """.creation_date <= '""" + end_time_formatted + """'
        AND """ + table_name + """.lang_tweet = "es"
        AND """ + table_name + """.has_keyword = 1
        AND """ + table_name + """.rt = 0
        """
    return (dbname, query)


def ms_to_date(ms):
    return datetime.datetime.fromtimestamp(ms / 1000.0)


def extract_tweets_around_sismic_events_espanol(verbose=0):
    '''
    Extractor de Tweets en torno a una hora de la ocurrencia de eventos sismiscos con magnitud +6
    Para los meses Jun, Jul y Ago del 2016
    '''
    manager = sql_to_json("localhost", 'root', '')

    #  Sismos de Junio en areas de habla hispana
    """
        2016-06-07T10:51:37.720Z,18.3637,-105.1731,10,6.3,mww,,56,1.383,1,us,us200062i1,2016-11-10T22:16:16.892Z,"106km SSW of San Patricio, Mexico",earthquake,5.5,1.7,,,reviewed,us,us
        2016-06-10T03:25:22.920Z,12.8318,-86.9633,10,6.1,mww,,39,0.159,1.04,us,us200063cy,2016-11-10T22:16:22.456Z,"22km E of Puerto Morazan, Nicaragua",earthquake,5.3,1.7,,,reviewed,us,us
    """
    '''
        Evento 1: 2016-06-07 10:51:37 Magnitud: 6.3 Mexico
        Evento 2: 2016-06-10 03:25:22 Magnitud: 6.1 Nicaragua
        '''
    database = "tweetsjun2016"
    queries = [
        """
        SELECT * FROM 20160607_tweets
        WHERE 20160607_tweets.creation_date >= '2016-06-07 9:51'
        AND 20160607_tweets.creation_date <= '2016-06-07 11:51'
        AND 20160607_tweets.lang_tweet = "es"
        AND 20160607_tweets.has_keyword = 1
        AND 20160607_tweets.rt = 0
        """,
        """
        SELECT * FROM 20160610_tweets
        WHERE 20160610_tweets.creation_date >= '2016-06-10 02:25'
        AND 20160610_tweets.creation_date <= '2016-06-10 04:25'
        AND 20160610_tweets.lang_tweet = "es"
        AND 20160610_tweets.has_keyword = 1
        AND 20160610_tweets.rt = 0
        """
    ]
    manager.mult_query_tweets(database, queries)

    #  Sismos de Julio en areas de habla hispana
    """
        2016-07-11T02:11:04.800Z,0.5812,-79.638,21,6.3,mww,,37,1.235,1.01,us,us100062hg,2016-11-10T22:17:10.794Z,"33km NW of Rosa Zarate, Ecuador",earthquake,4.4,1.5,,,reviewed,us,us
        2016-07-25T17:26:50.210Z,-26.1067,-70.5111,72,6.1,mww,,25,0.088,0.68,us,us20006hi2,2016-11-10T22:17:33.748Z,"54km WNW of Diego de Almagro, Chile",earthquake,4.9,1.7,,,reviewed,us,us
        """
    '''
        Evento 1: 2016-07-11 02:11:04 Magnitud: 6.3 Ecuador
        Evento 2: 2016-07-25 17:26:50 Magnitud: 6.1 Chile
    '''
    database = "tweetsjul2016"
    queries = [
        """
        SELECT * FROM 20160711_tweets
        WHERE 20160711_tweets.creation_date >= '2016-07-11 01:11'
        AND 20160711_tweets.creation_date <= '2016-07-11 03:11'
        AND 20160711_tweets.lang_tweet = "es"
        AND 20160711_tweets.has_keyword = 1
        AND 20160711_tweets.rt = 0
        """,
        """
        SELECT * FROM 20160725_tweets
        WHERE 20160725_tweets.creation_date >= '2016-07-25 16:26'
        AND 20160725_tweets.creation_date <= '2016-07-25 19:26'
        AND 20160725_tweets.lang_tweet = "es"
        AND 20160725_tweets.has_keyword = 1
        AND 20160725_tweets.rt = 0
        """
    ]
    manager.mult_query_tweets(database, queries)

    #  Sismos de Agosto en areas de habla hispana
    """
        2016-08-04T14:15:12.930Z,-22.3343,-66.0078,270,6.2,mww,,20,2.097,1.03,us,us10006a1d,2016-11-10T22:17:48.645Z,"49km WSW of La Quiaca, Argentina",earthquake,7.5,1.9,,,reviewed,us,us
        2016-08-18T18:09:43.940Z,-55.9035,-123.2414,10,6,mww,,50,27.905,0.95,us,us10006esj,2016-11-15T02:21:53.040Z,"Southern East Pacific Rise",earthquake,7.7,1.7,,,reviewed,us,us
    """
    '''
        Evento 1: 2016-08-04 14:15:12 Magnitud: 6.2 Argentina
        Evento 2: 2016-08-18 18:09:43 Magnitud: 6.0 Sur-Este del Oceano Pacifico
    '''
    database = "tweetsago2016"
    queries = [
        """
        SELECT * FROM 20160804_tweets
        WHERE 20160804_tweets.creation_date >= '2016-08-04 13:15'
        AND 20160804_tweets.creation_date <= '2016-08-04 15:15'
        AND 20160804_tweets.lang_tweet = "es"
        AND 20160804_tweets.has_keyword = 1
        AND 20160804_tweets.rt = 0
        """,
        """
        SELECT * FROM 20160818_tweets
        WHERE 20160818_tweets.creation_date >= '2016-08-18 17:09'
        AND 20160818_tweets.creation_date <= '2016-08-18 19:09'
        AND 20160818_tweets.lang_tweet = "es"
        AND 20160818_tweets.has_keyword = 1
        AND 20160818_tweets.rt = 0
        """]
    manager.mult_query_tweets(database, queries)


def extract_tweets_farofany_sismic_events_espanol(verbose=0):
    '''
    Extractor de Tweets en torno a una hora de la ocurrencia de eventos sismiscos con magnitud +6
    Para los meses Jun, Jul y Ago del 2016
    '''
    manager = sql_to_json("localhost", 'root', '')

    safe_ranges = inspect_sismos.getSafeTimeRanges()

    db_n_queries = []
    counter = 1
    for time_range in safe_ranges:
        start_t = ms_to_date(time_range[0])
        end_t = ms_to_date(time_range[1])
        (db, q) = build_db_n_query_for_sismic_spanish_non_rt_tweets(start_t, end_t, verbose=verbose)
        manager.connect_db(db)
        manager.query_tweets(q, "class0_" + str(counter), verbose=verbose)
        counter += 1
        manager.close()


if __name__ == "__main__":
    # extract_tweets_around_sismic_events_espanol()
    extract_tweets_farofany_sismic_events_espanol(verbose=1)
