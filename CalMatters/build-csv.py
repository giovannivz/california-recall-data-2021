import glob
import json
import pandas as pd
import os.path

yesno_rows = []
candidate_rows = []

for file in glob.glob('raw/*.json'):
    print(file)
    fparts = os.path.basename(file).split('_')

    try:
        f = open(file)
        js = json.load(f)
    except:
        f.close()
        js = None
        pass

    if js is None:
        continue

    for county, values in js['recall'].items():
        row = {}
        row['county'] = county
        row['yes_total'] = values['yes']['total']
        row['yes_percent'] = values['yes']['percent']
        row['no_total'] = values['no']['total']
        row['no_percent'] = values['no']['percent']
        row['updated'] = js['updated']
        row['download_timestamp'] = fparts[0]
        yesno_rows.append(row)

    counties = js['replace'][0]['results'].keys()

    for county in counties:
        row = {}

        for candidate in js['replace']:
            row['county'] = county
            row[candidate['name']] = candidate['results'][county]['total']
            row['updated'] = js['updated']
            row['download_timestamp'] = fparts[0]

        candidate_rows.append(row)

    f.close()

# save csv file
df = pd.DataFrame().from_records(yesno_rows)
df = df.sort_values(by=['download_timestamp', 'county'])
df = df.drop_duplicates(subset=[
    key for key in yesno_rows[0].keys() if key != 'download_timestamp'
])
df.to_csv('csv/calmatters-yesno.csv', index=False)
print(df)

# save csv file
df = pd.DataFrame().from_records(candidate_rows)
df = df.sort_values(by=['download_timestamp', 'county'])
df = df.drop_duplicates(subset=[
    key for key in candidate_rows[0].keys() if key != 'download_timestamp'
])
df.to_csv('csv/calmatters-candidates.csv', index=False)
print(df)