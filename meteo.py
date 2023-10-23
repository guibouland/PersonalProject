import pandas as pd
import requests
import json
import csv

# %%
"""
Daily data
"""
# Obention de l'API daily
url_daily = "https://api.open-meteo.com/v1/forecast?latitude=43.6109&longitude=3.8763&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&timezone=Europe%2FLondon"
response_daily = requests.get(url_daily)

# Vérification requête
if response_daily.status_code == 200:
    data_daily = response_daily.json()

    # Extraction des données
    tempmax = data_daily["daily"]["temperature_2m_max"]
    # print(tempmax)
    tempmin = data_daily["daily"]["temperature_2m_min"]

# Création Dataframe daily
df_daily = pd.DataFrame(data_daily)
# print(df_daily.iloc[:, -1])

pd.set_option("display.max_rows", None)

# Création du csv associé
df_daily.to_csv("df_daily.csv", index=False)

# %%
"""
Hourly data
"""

# Extraction API hourly data
url_hourly = "https://api.open-meteo.com/v1/forecast?latitude=43.6109&longitude=3.8763&hourly=temperature_2m&timezone=Europe%2FLondon"
response_hourly = requests.get(url_hourly)

# Vérification de l'url
if response_hourly.status_code == 200:
    data_hourly = response_hourly.json()

    # Extraction température hourly
    temphourly = data_hourly["hourly"]["temperature_2m"]
    # for i in range(len(temphourly)):
    #    print(temphourly[i])

# Création dataframe hourly
df_hourly = pd.DataFrame(data_hourly)

# Création du csv associé
df_hourly.to_csv("df_hourly.csv", index=False)


# %%
"""
Current data
"""
# Obtention API current data
url_current = "https://api.open-meteo.com/v1/forecast?latitude=43.6109&longitude=3.8763&current=temperature_2m,precipitation,weathercode,windspeed_10m&timezone=Europe%2FLondon"

response_current = requests.get(url_current)

# Vérification de l'url
if response_current.status_code == 200:
    data_current = response_current.json()

    # Extraction température hourly
    tempnow = data_current["current"]["temperature_2m"]
    precipnow = data_current["current"]["precipitation"]
    wmonow = data_current["current"]["weathercode"]
    windnow = data_current["current"]["windspeed_10m"]

# Création dataframe current
df_current = pd.DataFrame(data_current)

# Création csv associé
df_current.to_csv("df_current.csv", index=False)


# %%
"""
URL des images WMO codes
"""
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
# print(image_url(f"{data_current['current']['weathercode']}"))

# Boucle pour la liste daily
for item in data_daily["daily"]["weathercode"]:
    print(image_url(f"{item}"))

# WMO code pour current data
print(wmonow)
print(image_url(f"{wmonow}"))
