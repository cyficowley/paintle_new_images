import json

with open('urls.json') as json_data:
    urls = json.load(json_data)

with open('imagedata.json') as json_data:
    image_data = json.load(json_data)

ignore_list = [1,32,55,129,200,238,261,291,566,686,1115,1370,1356,1508,1502,1590,1673,1703,1739,1774,1792,1870,1946]

keys_str =  "objectid,accessioned,accessionnum,locationid,title,displaydate,beginyear,endyear,visualbrowsertimespan,medium,dimensions,inscription,markings,attributioninverted,attribution,provenancetext,creditline,classification,subclassification,visualbrowserclassification,parentid,isvirtual,departmentabbr,portfolio,series,volume,watermarks,lastdetectedmodification,wikidataid,customprinturl"

keys = keys_str.split(",")

key_to_idx = {key: i for i, key in enumerate(keys)}

keys_to_include = ["medium", "displaydate", "attribution", "title"]


final_list = []

for i, image in enumerate(image_data):
    if(i in ignore_list):
        continue
    
    image_datum = {}
    for key in keys_to_include:
        idx = key_to_idx[key]
        image_datum[key] = image[idx]
    
    final_list.append(image_datum)


with open('final_image_data.json', 'w') as f:
    json.dump(final_list, f)
