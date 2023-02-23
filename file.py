###  data.py  ###

import os, json

def compareData(data_json):
    FILE_PATH = os.path.abspath(".") + "/data.json"
    try:
        with open(FILE_PATH, mode="r", encoding="utf-8") as file:
            last_data_json = json.load(file)
    except Exception:
        last_data_json = {}
        with open(FILE_PATH, mode="w", encoding="utf-8") as file:
            file.write("")
    finally:
        if(last_data_json != data_json):
            with open(FILE_PATH, mode="w", encoding="utf-8") as file:
                json.dump(data_json, file)
    #----------------------------------------
    ids = data_json.keys()
    message_added=[]; message_deleted=[]
    for id in ids:
        present=[]; last=[]
        if (id in data_json.keys()):  # must be True
            for obj in data_json[id]:
                present += [obj["type"] + obj["id"]]
        if (id in last_data_json.keys()):
            for obj in last_data_json[id]:
                last += [obj["type"] + obj["id"]]
        added_data = list(set(present) - set(last))
        deleted_data = list(set(last) - set(present))
        #print(added_data, deleted_data)
        #--------------------
        if (id in data_json.keys()): # must be True
            message_one_course = ""
            for obj in data_json[id]:
                for data in added_data:
                    if(data == (obj["type"]+obj["id"])):
                        message_one_course += ("\n● " + obj["name"])
            message_added += [message_one_course]
        if (id in last_data_json.keys()):
            message_one_course = ""
            for obj in last_data_json[id]:
                for data in deleted_data:
                    if(data == (obj["type"]+obj["id"])):
                        message_one_course += ("\n● " + obj["name"])
            message_deleted += [message_one_course]
    #for message in message_added: print(message)
    #for message in message_deleted: print(message)
    #lose_ids = list(last_data_json.keys() - ids)
    return [message_added, message_deleted]