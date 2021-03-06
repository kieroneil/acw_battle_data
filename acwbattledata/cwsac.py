#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Build cwsac data """
import csv
import json
import os
import shutil
import sys
from os import path

from .utils import dict_subset

battle_fields = (  # 'cwsac_reference',
    'battle', 'url', 'battle_name', 'other_names', 'state', 'locations',
    'campaign', 'start_date', 'end_date', 'operation', 'assoc_battles',
    'results_text', 'result', 'forces_text', 'strength', 'casualties_text',
    'casualties', 'description', 'preservation', 'significance')


def battle_csv(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, battle_fields)
        writer.writeheader()
        for battle, battle_data in sorted(data.items()):
            row = dict_subset(battle_data, battle_fields)
            row['operation'] = int(row['operation'])
            if row['other_names']:
                row['other_names'] = '; '.join(row['other_names'])
            row['locations'] = '; '.join(x['place'] + ', ' + x['state']
                                         for x in battle_data['location'])
            writer.writerow(row)


belligerent_fields = [
    'battle',
    'belligerent',
    'description',
    'strength_min',
    'strength_max',
    'casualties',
    'killed',
    'wounded',
    'missing',
    'captured',
]


def forces_csv(data, filename):
    with open(filename, 'w', encoding='utf8') as f:
        writer = csv.DictWriter(f, belligerent_fields)
        writer.writeheader()
        for battle, battle_data in sorted(data.items()):
            for belligerent, x in sorted(battle_data['forces'].items()):
                row = dict_subset(x, belligerent_fields)
                row['battle'] = battle
                row['belligerent'] = belligerent
                writer.writerow(row)


commanders_fields = ('battle', 'belligerent', 'fullname', 'rank', 'navy',
                     'first_name', 'last_name', 'middle_name', 'suffix')


def commanders_csv(data, filename):
    with open(filename, 'w', encoding='utf8') as f:
        writer = csv.DictWriter(f, commanders_fields)
        writer.writeheader()
        for battle, battle_data in sorted(data.items()):
            for belligerent, x in sorted(battle_data['forces'].items()):
                for commander in x['commanders']:
                    row = commander.copy()
                    row['battle'] = battle
                    row['belligerent'] = belligerent
                    row['navy'] = int(row['navy'])
                    writer.writerow(row)


def copy_preservation(src, dst):
    shutil.copy(
        path.join(src, 'preservation.csv'),
        path.join(dst, 'cwsac_preservation.csv'))


def copy_significance(src, dst):
    shutil.copy(
        path.join(src, 'significance.csv'),
        path.join(dst, 'cwsac_significance.csv'))


def copy_theaters(src, dst):
    infile = path.join(src, 'theaters.csv')
    outfile = path.join(dst, 'cwsac_theaters.csv')
    fieldnames = ("theater", "dbp_resource", "dbp_category")
    with open(infile, 'r') as fp:
        data = list(csv.DictReader(fp))
    with open(outfile, 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames)
        writer.writeheader()
        for row in data:
            row['dbp_resource'] = f"http://dbpedia.org/resource/{row['dbp_resource']}"
            writer.writerow(row)


def copy_campaigns(src, dst):
    shutil.copy(
        path.join(src, 'campaigns.csv'), path.join(dst, 'cwsac_campaigns.csv'))


def copy_json(data, dst):
    with open(path.join(dst, 'cwsac.json'), 'w', encoding='utf8') as f:
        json.dump(data, f)


def build(src, dst):
    srcdir = path.join(src, "rawdata", "cwsac")
    data = {}
    json_dir = path.join(srcdir, 'json')
    for filename in os.listdir(json_dir):
        with open(path.join(json_dir, filename), 'r', encoding='utf8') as f:
            data[path.splitext(filename)[0]] = json.load(f)

    battle_csv(data, path.join(dst, 'cwsac_battles.csv'))
    forces_csv(data, path.join(dst, 'cwsac_forces.csv'))
    commanders_csv(data, path.join(dst, 'cwsac_commanders.csv'))
    copy_campaigns(srcdir, dst)
    copy_theaters(srcdir, dst)
    copy_significance(srcdir, dst)
    copy_preservation(srcdir, dst)
    copy_json(data, dst)


def main():
    src = sys.argv[1]
    dst = sys.argv[2]
    build(src, dst)


if __name__ == "__main__":
    main()
