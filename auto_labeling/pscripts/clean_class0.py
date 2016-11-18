import json

'''
User
    720531396486422528
        Posts alerts about any single sismo, need to delete its records
'''
print ("starting cleaning")
file_counter = 1
file_counter_lim = 56

excluded_users_id = [720531396486422528]

output_list = []
for file in range(file_counter_lim):
    file += 1
    filename = "class0_"+str(file)+".json"
    print("cleaning and merging file " + filename)
    try:
        with open("C:/Users/Vichoko/Documents/GitHub/real-time-twit/auto_labeling/pscripts/"+filename+".json") as readfile:
            data = json.load(readfile)
    except IOError:
        continue

    for row in data:
        if row[u'id_user'] in excluded_users_id:
            pass
        else:
            output_list.append(row)

j = json.dumps(output_list)
objects_file = "class0"+ ".json"
f = open(objects_file, 'w')
print >> f, j
print("	done")
