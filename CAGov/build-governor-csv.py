import glob
import json
import pandas as pd
import os.path

rows = []

for file in glob.glob('raw/governor/*'):
    print(file)
    fparts = os.path.basename(file).split('_')

    try:
        f = open(file)
        js = json.load(f)
    except:
        f.close()
        js = None

    if js is None or js.get('message', None):
        continue

    for county, values in js.items():
        row = {}
        row['county'] = county
        row['reporting'] = values['Reporting']

        for candidate in values['candidates']:
            row[candidate['Name']] = candidate['Votes']

        row['reporting_time'] = values['ReportingTime']
        row['download_timestamp'] = fparts[0]
        rows.append(row)

    f.close()

# save csv file
df = pd.DataFrame().from_records(rows)
df = df.sort_values(by=['download_timestamp', 'county'])
df = df.drop_duplicates(subset=[
    key for key in rows[0].keys() if key != 'download_timestamp'
])
df.to_csv('csv/cagov-governor.csv', index=False)
print(df)