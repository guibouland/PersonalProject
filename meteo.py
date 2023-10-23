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
    # Création Dataframe daily
    df_daily = pd.DataFrame(data_daily)
    print(df_daily.iloc[:, -1])

    pd.set_option("display.max_rows", None)

    # Création du csv associé
    df_daily.to_csv("df_daily.csv", index=False)

    # Extraction des données
    tempmax = data_daily["daily"]["temperature_2m_max"]
    tempmin = data_daily["daily"]["temperature_2m_min"]
    wmo_daily = data_daily["daily"]["weathercode"]
    sunrise = data_daily["daily"]["sunrise"]
    sunset = data_daily["daily"]["sunset"]
    uv = data_daily["daily"]["uv_index_max"]
    precip_daily_sum = data_daily["daily"]["precipitation_sum"]
    precip_proba_daily = data_daily["daily"]["precipitation_probability_max"]
    precip_hours_daily = data_daily["daily"]["precipitation_hours"]


# %%
"""
Hourly data
"""

# Extraction API hourly data
url_hourly = "https://api.open-meteo.com/v1/forecast?latitude=43.6109&longitude=3.8763&hourly=temperature_2m,windspeed_10m&timezone=Europe%2FLondon"
response_hourly = requests.get(url_hourly)

# Vérification de l'url
if response_hourly.status_code == 200:
    data_hourly = response_hourly.json()
    # Création dataframe hourly
    df_hourly = pd.DataFrame(data_hourly)

    # Création du csv associé
    df_hourly.to_csv("df_hourly.csv", index=False)
    # Extraction température hourly
    temp_hourly = data_hourly["hourly"]["temperature_2m"]
    # for i in range(len(temphourly)):
    #    print(temphourly[i])
    wind_hourly = data_hourly["hourly"]["windspeed_10m"]

    # Calcul vent moyen par jour sur les 7 prochain jour
    size = 24
    sub_lists = [
        wind_hourly[idx : idx + size] for idx in range(0, len(wind_hourly), size)
    ]

    def average_wind_daily():
        vent_moy = []
        for i in range(7):
            xmoy = sum(sub_lists[i]) / len(sub_lists[i])
            vent_moy.append(round(xmoy, 2))
        return vent_moy

    # Vent moyen par jour sur les 7 jours
    # print(average_wind_daily())

    # Changement écriture time (on enlève les dates avant les heures)
    time_hourly = []
    for i in range(len(df_hourly["hourly"]["time"])):
        time_hourly.append(df_hourly["hourly"]["time"][i][-5:])

    # print(time_hourly)


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

    # Création dataframe current
    df_current = pd.DataFrame(data_current)

    # Création csv associé
    df_current.to_csv("df_current.csv", index=False)

    # Extraction température hourly
    temp_now = data_current["current"]["temperature_2m"]
    precip_now = data_current["current"]["precipitation"]
    wmo_now = data_current["current"]["weathercode"]
    wind_now = data_current["current"]["windspeed_10m"]


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
# for item in range(len(wmo_daily)):
#     print(image_url(f"{wmo_daily[item]}"))

# WMO code pour current data
# print(image_url(f"{wmo_now}"))
