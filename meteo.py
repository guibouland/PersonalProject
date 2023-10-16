import pandas as pd
import requests
import json
import csv


# Obention de l'API
url = "https://api.open-meteo.com/v1/forecast?latitude=43.6109&longitude=3.8763&current=temperature_2m,precipitation,weathercode,windspeed_10m&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&timezone=Europe%2FLondon"
response = requests.get(url)

# Vérification requête
if response.status_code == 200:
    data = response.json()

    # données en ce moment
    tempnow = data["current"]["temperature_2m"]
    precipnow = data["current"]["precipitation"]
    windnow = data["current"]["windspeed_10m"]
    wcodenow = data["current"]["weathercode"]
    # températures journalières
    tempmax = data["daily"]["temperature_2m_max"]
    print(tempmax)
    tempmin = data["daily"]["temperature_2m_min"]


# Création Dataframe
df = pd.DataFrame(data)
print(df.iloc[:, -1], df.iloc[:, -3])

pd.set_option("display.max_rows", None)
df.to_csv("mon_dataframe.csv", index=False)

# Restructuration de la Dataframe


# Initialisation images WMO
with open("descriptions.json") as json_file:
    descriptions = json.load(json_file)


# Boucle d'images
for code_wmo, value in descriptions.items():
    description = value["description"]
    image_url = value["image"]
"""
    print(
        f"Code WMO : {code_wmo}, Description : {description}, URL de l'image : {image_url}\n"
    )
RENVOIE LE CODE WMO, LA DESCRIPTION ET L'URL DE L'IMAGE CORRESPONDANTE A AFFICHER
la description est pas forcément utile puisque c'est en anglais et que je cherche a faire un truc visuel
"""


def image_url(code_wmo):
    if code_wmo in descriptions:
        return descriptions[code_wmo]["image"]
    else:
        return "Code WMO non trouvé"


# Renvoie l'url de l'image du WMO
print(image_url(f"{data['current']['weathercode']}"))

# Boucle pour la liste daily
for item in data["daily"]["weathercode"]:
    print(image_url(f"{item}"))
