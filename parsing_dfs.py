import json
import pandas as pd


with open('etl-pipeline-photos/print.json') as f:
    json_data = json.load(f)

photoDetailsDF = pd.DataFrame()
facesDetailsDF = pd.DataFrame()
salientregionDetailsDF = pd.DataFrame()
featuresDetailsDF = pd.DataFrame()
printbook_metadataDF = pd.DataFrame()

print_key = json_data["print"]

printbook_metadata = {}
uuid = print_key["uuid"]
printbook_metadata["uuid"] = uuid
printbook_metadata["product_code"] = print_key["product_code"]
printbook_metadata["title"] = print_key["title"]

printbook_metadataDF = pd.DataFrame.from_dict([printbook_metadata])

for pr in json_data: # looping over prints
    for pg in print_key["pages"]: # looping over pages for each print
        try:
            elements = pg["elements"]
            for ele in elements:                                 
                photodetails = {}
                try :
                    #Information of photos contained within a print such as dates and size taken  
                    photoDF = pd.json_normalize(ele["photo"]["selected_location"])                                  
                    photoDF["photo_identifier_hash"] = ele["photo"]["photo_identifier_hash"] 
                    photoDF1 = photoDF[['photo_identifier_hash','photo_taken_at','photo_modified_at']]                 
                    photoDetailsDF = photoDetailsDF.append(photoDF1,ignore_index=True)
                except  KeyError as e: 
                    # TODO: Handle the exception properly
                    pass   
                
                try:
                    # faces positions
                    facesDF = pd.json_normalize(ele["photo"]["selected_location"]["analysis"]["faces"])
                    facesDF["photo_identifier_hash"] = ele["photo"]["photo_identifier_hash"]
                    facesDF1 = facesDF[['photo_identifier_hash','bounding_position_x','bounding_position_y','bounding_position_width','bounding_position_height','detection_confidence']]   
                    facesDetailsDF = facesDF1.append(facesDetailsDF,ignore_index=True)
                except  KeyError as e: 
                    # TODO: Handle the exception properly
                    pass

                try:  
                    #Salient Region
                    salientregionDF = pd.json_normalize(ele["photo"]["selected_location"]["analysis"]["salient_region"])
                    salientregionDF["photo_identifier_hash"] = ele["photo"]["photo_identifier_hash"]
                    salientregionDF1 = salientregionDF[['photo_identifier_hash','top_x_percent','top_y_percent','width_percent','height_percent']]   
                    salientregionDetailsDF = salientregionDetailsDF.append(salientregionDF1,ignore_index=True)
                except KeyError as e:
                    # TODO: Handle the exception properly
                    pass    
                
                try:  
                    #Classification features of the photo
                    featuresDF = pd.json_normalize(ele["photo"]["selected_location"]["analysis"]["features"]["features"])
                    featuresDF["photo_identifier_hash"] = ele["photo"]["photo_identifier_hash"]
                    featuresDF1 = featuresDF[['photo_identifier_hash','label','confidence']]   
                    featuresDetailsDF = featuresDetailsDF.append(featuresDF1,ignore_index=True)
                except KeyError as e:
                    # TODO: Handle the exception properly
                    pass  

        except KeyError as e:        
            # TODO: Handle the exception properly
            pass
        
print(printbook_metadataDF)      
print(photoDetailsDF)
print(facesDetailsDF)
print(salientregionDetailsDF)
print(featuresDetailsDF)



