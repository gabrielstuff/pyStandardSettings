#!/usr/bin/env python
import json
import argparse
from dotmap import DotMap
import collections

settings_files = ["settings/settings.default.json", "settings/settings.json"]
settings = {}

def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

try:
  with open(settings_files[0]) as settings_file:
      nestedArguments = json.load(settings_file)
except IOError:
  pass
arguments = []

def addArgument(d, pre='--'):
  for k, v in d.iteritems():
    if isinstance(v, dict):
      addArgument(v, pre + k + '.')
    else:
      arguments.append(pre + k)

addArgument(nestedArguments)

# init parser
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--settings', help='settings file in json format')
for argument in arguments:
  parser.add_argument(argument)

# parse
args = parser.parse_args()
if args.settings:
  settings_files.append(args.settings)

# get settings
for file in settings_files:
  try:
    with open(file) as setting_file:
        dict_merge(settings, json.load(setting_file))
  except IOError:
    pass

parsedArgs = {}

for k, v in vars(args).iteritems():
  if v is not None:
    parent = parsedArgs
    keys = k.split('.')
    for key in keys[:-1]:
      if key not in parent:
        parent[key] = {}
      parent = parent[key]
    parent[keys[-1]] = v

print parsedArgs
dict_merge(settings, parsedArgs)
settings = DotMap(settings)

