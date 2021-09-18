import json
import glob
import os
import os.path

files = glob.glob('raw/*/*')

for file in files:
    if not os.path.isfile(file):
        continue

    with open(file) as f:
        try:
            js = json.load(f)
        except json.decoder.JSONDecodeError as e:
            # can't open json
            print(file, e)
            os.unlink(file)