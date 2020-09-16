import os
import json
import datetime


def dump_api_response(data,route):

    # You should change 'test' to your preferred folder.
    path = ("data/")
    check = os.path.isdir(path)
    if not check:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        print(path, "folder already exists.")

    date = datetime.datetime.now().strftime("%Y-%m-%dT_%H:%M:%S.%f")
    dumpfile=(path + route + '_' + date +'.json')

    with open(dumpfile, 'w') as json_file:
        json.dump(data, json_file)

    return
