from flask import Flask, request
import logging
import os
import json
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str)
parser.add_argument("--port", type=str)
parser.add_argument("--filename", type=str)
parser.add_argument("--choice", type=str)

args = parser.parse_args()
app = Flask(__name__)


def get_csv(csv_file_name):
    with open(csv_file_name, encoding="utf-8") as csv_file:
        data = list(list(list(list(list(list(csv.DictReader(csv_file, delimiter=';')))))))
    return data


@app.route('/arrest', methods=['GET'])
def main():
    date = get_csv(args.filename)
    print(date)
    if args.choice == "blame":
        response = [{i["surname"] + " " + i["first_name"]: i["charge"]} for i in list(date)]
    else:
        response = [{i["surname"] + " " + i["first_name"]: i["date"]} for i in list(date)]
    print(response)
    type_list = set([j.values() for j in response])
    print(type_list)
    return ""
    #json.dumps(response)


if __name__ == '__main__':
    print(args.host, args.port, args.filename, args.choice)
    port = int(os.environ.get("PORT", int(args.port)))
    app.run(host=args.host, port=port)
