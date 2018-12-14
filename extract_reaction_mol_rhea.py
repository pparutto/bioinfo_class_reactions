#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 18:28:43 2018

@author: pierre
"""

import argparse

class Participant:
    def __init__(self):
        self.left = []
        self.right = []


def read_participant(f):
    line = f.readline()
    cmpd_name = None
    stoichio = None
    while line != '' and not line.startswith("</bp:physicalEntityParticipant>"):
        if line.startswith(" <bp:PHYSICAL-ENTITY"):
            cmpd_name = line.split('"')[1].split(":")[1]
        elif line.startswith(" <bp:STOICHIOMETRIC-COEFFICIENT"):
            stoichio = float(line.split(">")[1].split("<")[0])
        line = f.readline()
    return [cmpd_name, stoichio]


def read_reaction(f):
    line = f.readline()
    particip = Participant()
    while line != '' and not line.startswith("</bp:biochemicalReaction>"):
        if line.startswith(" <bp:LEFT"):
            particip.right.append(line.split('.')[1])
        elif line.startswith(" <bp:RIGHT"):
            particip.left.append(line.split('"')[1])
        line = f.readline()
    return particip


parser = argparse.ArgumentParser(description="Extract reactions equation\
 from owl file")
parser.add_argument("owl_file", help="path to a rhea owl file")

args = parser.parse_args()

particips = {}
reacts = {}
with open(args.owl_file, 'r') as f:
    line = f.readline()
    while line != '':
        if line.startswith('<bp:physicalEntityParticipant'):
            p_id = line.split('"')[1]
            particips[p_id] = read_participant(f)
        elif line.startswith('<bp:biochemicalReaction'):
            reac_id = line.split("/")[4].split('"')[0]
            reacts[reac_id] = read_reaction(f)
        line = f.readline()

for reac_name, particip in reacts.items():
    res = reac_name + " "
    res += "+".join([str(particips[p][1]) + ":" + str(particips[p][0])
            for p in particip.left])
    res += "="
    res += "+".join([str(particips[p][1]) + ":" + str(particips[p][0])
            for p in particip.right])
    print(res)
print("lol")
