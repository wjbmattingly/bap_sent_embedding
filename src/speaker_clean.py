import json
import glob

files = glob.glob(f"./data/data_saha/*/*/*.json")
speakers = []
for filename in files:
    with open (filename, "r") as f:
        data = json.load(f)
    tmp = data["header"]["speakers"]
    for t in tmp:
        speakers.append(t)
speakers = list(set(speakers))
speakers.sort()
with open ("data/all_speakers.json", "w") as f:
    json.dump(speakers, f, indent=4)
