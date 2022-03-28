import json
import requests


def repair(host, port, **args):
    server_json = requests.get(host + ":" + port).json()
    data = json.load(server_json)
    data_keys = data.keys()
    return_dict = {"available": [], "unavailable": []}
    for i in args.keys():
        if i not in data_keys:
            return_dict["unavailable"].append(i)
            continue
        if data[i] < args[i]:
            return_dict["unavailable"].append(i)
            continue
        return_dict["available"].append(i)
    return_dict["available"] = sorted(return_dict["available"], reverse=True)
    return_dict["unavailable"] = sorted(return_dict["unavailable"], reverse=True)
    return return_dict
