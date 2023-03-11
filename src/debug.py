import pickle

with open("skip_dict.pkl", 'rb') as f:
    skipdict = pickle.load(f)

for key, val in skipdict.items():
    if ('he' in key or 'p63' in key) and type(val) == dict:
        skipdict[key]['done'] = False
