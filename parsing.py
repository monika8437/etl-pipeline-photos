import os
import json
import pandas as pd
from flatten_json import flatten

# os.system('cls')

with open('etl-pipeline-photos/print.json') as f:
    json_data = json.load(f)

"""
store photobook metadata
"""
print_key = json_data["print"]

final_db_dict = {}

printbook_metadata = {}
uuid = print_key["uuid"]
printbook_metadata["uuid"] = uuid
printbook_metadata["product_code"] = print_key["product_code"]
printbook_metadata["title"] = print_key["title"]

# print(printbook_metadata)

"""
Information of photos contained within a print such as dates and size taken
"""

list_of_photo_sizes = []
list_of_photo_classification =[]
list_of_face_positions = []
list_of_salient_regions = []


pages = print_key["pages"]
for p in pages:
    if p["product_layout_tag"] not in ["layout-blank-front","layout-blank-back","layout-back","layout-blank-front","layout-blank-back"]:
        elements = p["elements"] # list of dict
        for e in elements: # dict
            if "photo" in e:
                photo = e["photo"]
                if "popsa_location" in photo:
                    popsa_location = photo["popsa_location"]
                    original = popsa_location["original"]
                    width_pixels = original["width_pixels"]
                    height_pixels = original["height_pixels"]
                selected_location = photo["selected_location"]
                photo_taken_at = selected_location["photo_taken_at"]
                photo_modified_at = selected_location["photo_modified_at"]
                photo_identifier_hash = photo["photo_identifier_hash"]

                photo_size_date_dict = {}
                photo_size_date_dict["uuid"] = uuid
                photo_size_date_dict["photo_identifier_hash"] = photo_identifier_hash
                photo_size_date_dict["width_pixels"] = width_pixels
                photo_size_date_dict["height_pixels"] = height_pixels
                photo_size_date_dict["photo_taken_at"] = photo_taken_at
                photo_size_date_dict["photo_modified_at"] = photo_modified_at

                list_of_photo_sizes.append(photo_size_date_dict)
 
            """
            Classification features of the photo
            """
            classification = {}
            analysis = selected_location["analysis"]
            features = analysis["features"]["features"] #This is a list
            classification["uuid"] = uuid
            classification["photo_identifier_hash"] = photo_identifier_hash
            for f in features: # this gives a dict
                classification[f["label"]] = f["confidence"]
            
            list_of_photo_classification.append(classification)

            """
            Face positions
            """
            analysis = selected_location["analysis"] # returns dict
            if "faces" in analysis:
                faces = analysis["faces"] #returns list
                face_position = {}
                for f in faces: # returns a dict
                    face_position["uuid"] = uuid
                    face_position["photo_identifier_hash"] = photo_identifier_hash
                    for key,value in f.items():
                        face_position[key] = value
                    list_of_face_positions.append(face_position)

            """
            Salient Region
            """
            salient_region = analysis["salient_region"] #returns dict
            print(salient_region)
            regions = {}
            regions["uuid"] = uuid
            regions["photo_identifier_hash"] = photo_identifier_hash
            for key,value in salient_region.items():
                regions[key] = value
            list_of_salient_regions.append(regions)


print("+++++++++++++++printing photo sizes +++++++++++++++")
print(list_of_photo_sizes)
print("+++++++++++++++printing photo classification +++++++++++++++")
print(list_of_photo_classification)
print("+++++++++++++++printing face positions +++++++++++++++")
print(list_of_face_positions)
print("+++++++++++++++printing salient regions +++++++++++++++")
print(list_of_salient_regions)