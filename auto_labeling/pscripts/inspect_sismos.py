import json

def getSafeTimeRanges():
    with open("C:/Users/Vichoko/Documents/GitHub/real-time-twit/auto_labeling/sismos_5+_jun-ago_LA.json") as readfile:
        data = json.load(readfile)

    event_count = data['metadata']['count']

    starting_times_list = []
    for event_index in range(event_count):
        starting_times_list.append(data['features'][event_index]['properties']['time'])

    ## Need a list of tuples (start_time, end_time) that can assure that no sismic tweets will appear
    # Criteria:
    '''
        safe_ranges = []
        For a sismic event 'e':
            safe_tweet_range = (e.start_time - <35 Mins>, e.start_time - <30 Min>)
            if (for all sismic events o_s { o_s.start_time /not_in sage_tweet_range})
                safe_ranges.append(safe_tweet_range)
    '''

    safe_ranges = []
    for event_start_time in starting_times_list:
        i = event_start_time - 35*(60*1000)
        j = event_start_time - 30*(60*1000)

        valid = 1
        for other_event_start_time in starting_times_list:
            # Si existe evento que calze dentro del rango, lo invalido
            if i < other_event_start_time < j:
                valid = 0
        if valid:
            safe_ranges.append((i, j))


    print(safe_ranges)
    print(len(safe_ranges))
    return safe_ranges