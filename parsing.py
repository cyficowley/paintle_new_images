import csv
import json
import random
import webbrowser
import numpy as np

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

totals = {}


def print_identifiers(keys, val):
    print(json.dumps({k:v for k,v in zip(keys,val)}))


def filter_data(keys_to_idx, data, key, val):
    key_idx = keys_to_idx[key]
    new_data = [each for each in data if each[key_idx] == val]
    return new_data

def get_field(keys_to_idx, datum, key):
    key_idx = keys_to_idx[key]
    return datum[key_idx]

def update_res(url, new_res):
    return url.replace("!200,200", f"!{new_res},{new_res}")

    
with open('data/objects.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    data = list(csv_reader)

with open('data/published_images.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    images = list(csv_reader)

keys = data[0]
vals = data[1:]
keys_to_idx = {}
for i, key in enumerate(keys):
    keys_to_idx[key] = i

clas_idx = keys_to_idx["classification"]

for each in vals:
    clas = each[clas_idx]
    if clas in totals:
        totals[clas] += 1
    else:
        totals[clas] = 1
print(totals)



painting_data = filter_data(keys_to_idx, vals, "classification", "Painting")

print(len(painting_data))

image_id_to_data = {}

for image in images:
    image_id_to_data[image[10]] = image

    

# random.shuffle(painting_urls)

# for each in painting_urls[:30]:
#     url = update_res(each, 1000)
#     webbrowser.open(url, new=0, autoraise=True)

# for each in vals[:3]:
#     print_identifiers(keys, each)


lengths = []
for painting in painting_data:
    lengths.append(len(get_field(keys_to_idx, painting, "provenancetext")))


percentiles = [5, 25, 50, 75, 95]
results = np.percentile(lengths, percentiles)
print("before probs ", results)


sorted_painting_data = [v for _, v in sorted(zip(lengths, painting_data))]





weights = np.array(lengths)
probabilities = weights / weights.sum()

ids = [i for i in range(len(painting_data))]

# Sample without replacement
sampled_ids = np.random.choice(ids, size=len(painting_data) // 2, replace=False, p=probabilities)

sampled_paintings = [painting_data[i] for i in sampled_ids]


print(len(sampled_paintings))




lengths = []
for painting in sampled_paintings:
    lengths.append(len(get_field(keys_to_idx, painting, "provenancetext")))


percentiles = [5, 25, 50, 75, 95]
results = np.percentile(lengths, percentiles)
print("after probs ", results)


painting_urls = []
final_painting_data = []
for painting in sampled_paintings:
    obj_id = get_field(keys_to_idx, painting, "objectid")
    if(obj_id in image_id_to_data):
        image = image_id_to_data[obj_id]
        painting_urls.append(update_res(image[2], 1000))
        final_painting_data.append(painting)

with open('urls.json', 'w') as f:
    json.dump(painting_urls, f)

with open('imagedata.json', 'w') as f:
    json.dump(final_painting_data, f)

