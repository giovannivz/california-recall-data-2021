import json
import glob
import os

files = glob.glob('raw/*.json')

for file in files:
    fn = None

    with open(file) as f:
        try:
            js = json.load(f)
            fn = f"raw/NYT-2021-california-recall_{js['meta']['timestamp']}_{js['meta']['version']}.json"
        except:
            pass

    if fn is not None:
        print(f"{file} -> {fn}")
        os.rename(file, fn)
