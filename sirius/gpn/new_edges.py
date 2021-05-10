import json
import pandas as pd


with open("result.json", "r") as f:
    data = json.load(f)

df = pd.read_csv("corr_matrix.csv")

new_edges = []

for i in df.index:
    for j in df.columns:
        if df.loc[i, j] < 0.165 and df.loc[i, j] != 0:
            new_edges.append({
                "from": i,
                "to": j
            })

data["edges"] = data["edges"] + new_edges

print(len(new_edges))

with open("gpn.json", "w") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)