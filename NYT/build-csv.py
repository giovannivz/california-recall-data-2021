import glob
import json
import pandas as pd

data = {}
sorting = {
    'race': ['meta_version'],
    'candidates': ['candidate_id', 'meta_version'],
    'counties': ['name', 'meta_version']
}

for file in glob.glob('raw/*.json'):
    print(file)

    try:
        f = open(file)
        js = json.load(f)
    except:
        f.close()
        js = None

    if js is None:
        continue

    for item in js['data']['races']:
        race_id = item['race_id']

        # gather overall race stats
        if data.get(race_id, None) is None:
            data[race_id] = {'race': [], 'candidates': [], 'counties': []}

        row = {
            k: v
            for k,v in item.items()
            if type(v) is not list and type(v) is not dict
        }

        row['meta_version'] = js['meta']['version']
        row['meta_track'] = js['meta']['track']
        row['meta_timestamp'] = js['meta']['timestamp']

        data[race_id]['race'].append(row)

        # gather candidate stats directly
        for candidate in item['candidates']:
            row = candidate

            row['last_updated'] = item['last_updated']
            row['meta_version'] = js['meta']['version']
            row['meta_track'] = js['meta']['track']
            row['meta_timestamp'] = js['meta']['timestamp']

            data[race_id]['candidates'].append(row)

        # gather county stats
        for county in item['counties']:
            row = {}

            # copy directly and flatten any dicts (results, results_absentee)
            for k, v in county.items():
                if type(v) is dict:
                    for kk, vv in v.items():
                        row[f"{k}_{kk}"] = vv
                else:
                    row[k] = v

            row['last_updated'] = item['last_updated']
            row['meta_version'] = js['meta']['version']
            row['meta_track'] = js['meta']['track']
            row['meta_timestamp'] = js['meta']['timestamp']

            data[race_id]['counties'].append(row)

    f.close()

# save csv file
for race_id, race in data.items():
    for type, values in race.items():
        fn = f"csv/{race_id}-{type}.csv"
        df = pd.DataFrame().from_records(values)
        df = df.sort_values(by=sorting[type])
        df.to_csv(fn, index=False)
        print(df)