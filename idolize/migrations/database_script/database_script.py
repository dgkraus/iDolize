import json
import os

from django.db import migrations, transaction

from idolize.models import IdolDatabase

# script for one-time population of database based on data gathered via webscraper

def populate_database():
    # give the path to the main folder that contains all the json files, then iterate through the folders and append all the file locations into a list
    script_path = r"C:\Users\denni\Desktop\Projects\idolize\idolize\migrations\idol_dicts"
    json_files = []
    for root, dirs, files in os.walk(script_path):
        for file in files:
            if file.endswith("json"):
                json_files.append(os.path.join(root,file))
    
    json_data = []
    for file in json_files:
        with open(file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            json_data.append(data)

    field_name = IdolDatabase._meta.get_fields()
    actual_names = [field.name for field in field_name]
    idol_list = []

    for dict in json_data:
        idol_name = dict.get("idol_name", "").replace("_", " ") #because this got saved in a slightly different format in the webscraper, it needs to be reformatted
        nickname = dict.get("nickname", "")
        birthdate = dict.get("birthdate", "")
        birthplace = dict.get("birthplace", "")
        zodiac = dict.get("zodiac", "")
        height = dict.get("height", "").replace(" cm","")
        sns = dict.get("sns", [])

        # I originally saved the SNS links in a Python list with my webscraper, which turned out to make it difficult to retrieve again once saved in the SQLite database;
        # manually changing the formatting at this point saves some trouble later.
        sns_dict = {}
        for link in sns:
            if "twitter" in link or "x.com" in link:
                sns_dict["Twitter"] = link
            elif "instagram" in link:
                sns_dict["Instagram"] = link
            elif "tiktok" in link:
                sns_dict["TikTok"] = link

        idol = IdolDatabase(
                idol_name = idol_name,
                nickname = nickname,
                birthdate = birthdate,
                birthplace = birthplace,
                zodiac = zodiac,
                height = height,
                sns = sns_dict,
    )
        idol_list.append(idol)

    existing_db_entries = set(IdolDatabase.objects.values_list("idol_name", flat=True))

    # bulk_create raises an error if any of the entries to be created is not unique (because the idol_name CharField is set as unique). setting the bulk_create
    # to ignore_conflicts=True is also possible, but this an easy way to create a print statement for debug purposes
    filtered_idol_list = [
        idol for idol in idol_list if idol.idol_name not in existing_db_entries]
    
    if filtered_idol_list:
        try:
            with transaction.atomic():
                IdolDatabase.objects.bulk_create(filtered_idol_list)
        except Exception as e:
            print(f"Error occurred during bulk_create: {e}")
            raise
    else:
        print("no new unique entries to create")

populate_database()