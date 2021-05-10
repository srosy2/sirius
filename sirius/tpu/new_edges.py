import json
import pandas as pd


with open("tpu.json", "r") as f:
    data = json.load(f)

df = pd.read_csv("corr_matrix.csv")

new_edges = []

iterator = 0
for i in df.index:
    for j in df.columns:
        if float(df.loc[i, j]) < 0.16 and float(df.loc[i, j]) != 0:
            to = j
            if iterator % 4 == 0:
                to = int(to)
            new_edges.append({
                "from": i,
                "to": to
            })
            iterator += 1

data["edges"] = data["edges"] + new_edges

print(len(new_edges))

with open("tpu1.json", "w") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)