#!/usr/bin/env python3
import csv
import datetime
import fnmatch
import json
import os
import sys
from os import path

import yaml

BASE_URL = "http://www.nps.gov/abpp/shenandoah/"


def load_data(src):
    data = []
    for filename in os.listdir(path.join(src, "yaml")):
        if fnmatch.fnmatch(filename, "*.yaml"):
            fn = path.join(src, "yaml", filename)
            with open(fn, 'r', encoding="utf8") as f:
                d = yaml.load(f)
                d['url'] = BASE_URL + path.basename(
                    path.splitext(fn)[0]) + '.html'
                data.append(d)
    return data


def clean_battle(battle):
    row = {}
    if 'Number' not in battle:
        print(battle['Battle'])
    row['battle_id'] = battle['Number']
    row['battle_name'] = battle['Battle']
    row['cwsac_id'] = battle['CWSAC']
    row['start_date'] = datetime.datetime.strptime(battle['Start Date'], "%d %B %Y").\
        strftime("%Y-%m-%d")
    try:
        row['end_date'] = datetime.datetime.strptime(battle['End Date'], "%d %B %Y").\
            strftime("%Y-%m-%d")
    except KeyError:
        row['end_date'] = row['start_date']
    row['campaign'] = battle['Campaign']
    row['county'] = ';'.join(x['name'] + ', ' + x['state']
                             for x in battle['County'])
    row['url'] = battle['url']
    return row


def build_battles(data, dst):
    battles = [clean_battle(x) for x in data]
    fieldnames = ('battle_id', 'battle_name', 'cwsac_id', 'start_date',
                  'end_date', 'campaign', 'county', 'url')
    dst_file = path.join(dst, 'shenandoah_battles.csv')
    with open(dst_file, 'w', encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(battles)
    print("Writing: %s" % dst_file)


def clean_forces(battle):
    forces = []
    for i in ("U", "C"):
        x = {}
        x["battle_id"] = battle["Number"]
        if i == "U":
            x["belligerent"] = "US"
        else:
            x["belligerent"] = "Confederate"
        x['description'] = battle["Forces Engaged"][i]["text"]
        try:
            x['strength_min'] = battle["Forces Engaged"][i]["strength_min"]
            x['strength_max'] = battle["Forces Engaged"][i]["strength_max"]
        except KeyError:
            x['strength_min'] = battle["Forces Engaged"][i]["strength"]
            x['strength_max'] = battle["Forces Engaged"][i]["strength"]
        x['casualties_text'] = battle["Casualties"][i]["text"]
        for j in ("casualties", "killed", "wounded", "missing_captured"):
            x[j] = battle["Casualties"][i][j]
        forces.append(x)
    return forces


def build_forces(data, dst):
    fieldnames = ('battle_id', 'belligerent', 'description', 'strength_min',
                  'strength_max', 'casualties_text', 'casualties', 'killed',
                  'wounded', 'missing_captured')
    dst_file = path.join(dst, 'shenandoah_forces.csv')
    with open(dst_file, 'w', encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for battle in data:
            writer.writerows(clean_forces(battle))
    print("Writing: %s" % dst_file)


def clean_commanders(battle):
    ret = []
    for i in ("U", "C"):
        x = {}
        x["battle_id"] = battle["Number"]
        x["cwsac_id"] = battle["CWSAC"]
        if i == "U":
            x["belligerent"] = "US"
        else:
            x["belligerent"] = "Confederate"
        commanders = battle["Principal Commanders"][i]
        for cmdr in commanders:
            for j in ("last_name", "first_name", "middle_name", "rank"):
                try:
                    x[j] = cmdr[j]
                except KeyError:
                    x[j] = None
        ret.append(x)
    return ret


def build_commanders(data, dst):
    fieldnames = ('battle_id', 'cwsac_id', 'belligerent', 'last_name',
                  'first_name', 'middle_name', 'rank')
    dst_file = path.join(dst, 'shenandoah_commanders.csv')
    with open(dst_file, 'w', encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for battle in data:
            writer.writerows(clean_commanders(battle))
    print("Writing: %s" % dst_file)


def build_json(data, dst):
    dst_file = path.join(dst, 'shenandoah.json')
    with open(dst_file, 'w', encoding="utf8") as f:
        json.dump(data, f)
    print("Writing: %s" % dst_file)


def build(src, dst):
    print("Building Shenandoah data")
    srcdir = path.join(src, "rawdata", "shenandoah")
    data = load_data(srcdir)
    build_battles(data, dst)
    build_forces(data, dst)
    build_commanders(data, dst)
    build_json(data, dst)


def main():
    src, dst = sys.argv[1:3]
    build(src, dst)


if __name__ == "__main__":
    main()
