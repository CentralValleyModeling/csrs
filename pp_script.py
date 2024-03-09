import json
import urllib.request

import pandas as pd

response = urllib.request.urlopen(
    "http://127.0.0.1:8000/annual_exceedance/dv/b/S_SHSTA?year_type=cy"
)
payload = json.loads(response.read())


frames = list()
for study, values in payload.items():
    df = pd.DataFrame.from_records(values, columns=["EXCEEDANCE", study])
    df = df.set_index("EXCEEDANCE")
    frames.append(df)
df = pd.concat(frames, axis=1)
print(df)
