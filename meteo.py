import pandas as pd
import requests
import json
import csv
from datetime import datetime, timedelta, date
from IPython.display import HTML


# %%
"""
Daily data
"""
# Obention de l'API daily
url_daily = "https://api.open-meteo.com/v1/meteofrance?latitude=43.6109&longitude=3.8763&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_hours,precipitation_probability_max,winddirection_10m_dominant&timezone=Europe%2FLondon"
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
    precip_daily_sum = data_daily["daily"]["precipitation_sum"]
    precip_hours_daily = data_daily["daily"]["precipitation_hours"]
    wind_direc_daily = data_daily["daily"]["winddirection_10m_dominant"]

Date = pd.to_datetime(data_daily["daily"]["time"])
Date = [datetime.strftime(a, "%A %d/%m") for a in Date]
print(Date[1][:-5])
print(Date[0][-5:])
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
    wind_hourly = data_hourly["hourly"]["windspeed_10m"]

    # Calcul vent moyen par jour sur les 7 prochain jour
    size = 24
    # On crée 7 sous-listes de taille 24 contenant les valeurs des 24 heures par jours, fois 7
    sub_lists = [
        wind_hourly[idx : idx + size] for idx in range(0, len(wind_hourly), size)
    ]

    def average_wind_daily():
        vent_moy = []
        for i in range(7):
            for j in sub_lists[i]:
                if j == None:
                    # On retire les éléments de chaque sous listes qui ne sont pas conformes ("None")
                    del sub_lists[i][j]
            # On calcule la moyenne de chaque sous-listes en prenant compte des changements s'il y a un manque de donnée (le len diminue)
            xmoy = sum(sub_lists[i]) / len(sub_lists[i])
            # On ajoute chaque moy à une nouvelle liste qui donnera les vents moyens
            vent_moy.append(round(xmoy, 2))
        return vent_moy

    # Changement écriture time (on enlève les dates avant les heures)
    time_hourly = []
    for i in range(len(df_hourly["hourly"]["time"])):
        time_hourly.append(df_hourly["hourly"]["time"][i][-5:])

vent_moy = average_wind_daily()
print(vent_moy)
# %%
"""
Current data
"""
# Obtention API current data
url_current = "https://api.open-meteo.com/v1/forecast?latitude=43.6109&longitude=3.8763&current=temperature_2m,precipitation,weathercode,windspeed_10m,winddirection_10m&timezone=Europe%2FLondon"

response_current = requests.get(url_current)

# Vérification de l'url
if response_current.status_code == 200:
    data_current = response_current.json()

    # Création dataframe current
    df_current = pd.DataFrame(data_current)
    # print(df_current.iloc[:, -1])

    # Création csv associé
    df_current.to_csv("df_current.csv", index=False)

    # Extraction data current
    date_now = data_current["current"]["time"][:10]
    # print(date_now)
    temp_now = data_current["current"]["temperature_2m"]
    precip_now = data_current["current"]["precipitation"]
    wmo_now = data_current["current"]["weathercode"]
    strwmonow = f"{wmo_now}"
    wind_now = data_current["current"]["windspeed_10m"]
    wind_direc_now = data_current["current"]["winddirection_10m"]


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


# %%
"""
NOW
"""
from IPython.display import Markdown, display, HTML
from PIL import Image
from tabulate import tabulate

# Affichage des images
imagenow = image_url(strwmonow)
respnow = requests.get(imagenow, stream=True)
imgnow = Image.open(respnow.raw)
# display(imgnow): à utiliser dans le qmd

# Tableau
datanow = [
    [
        date_now,
        temp_now,
        precip_now,
        wind_now,
        wind_direc_now,
    ]
]
headersnow = ["Date", "Température", "Précipitations", "Vent", "Direction"]
tablenow = tabulate(datanow, headersnow, showindex=False, tablefmt="pipe")

# display(Markdown(tablenow)) à utiliser dans le qmd

# %%
"""
SPACE USED FOR BLACK
"""

# Initialisation WMO images
with open("descriptions.json", "r") as json_file:
    descriptions = json.load(json_file)


# Images loop
for code_wmo, value in descriptions.items():
    description = value["description"]
    image_url = value["image"]


# Function that returns the image URL
def image_url(code_wmo):
    if code_wmo in descriptions:
        return descriptions[code_wmo]["image"]
    else:
        return "WMO code not found"


# %%
"""
DATA NOW
"""

# Current data API extraction
url_current = "https://api.open-meteo.com/v1/meteofrance?latitude=43.6109&longitude=3.8763&current=temperature_2m,precipitation,weathercode,windspeed_10m,winddirection_10m&timezone=Europe%2FLondon"

response_current = requests.get(url_current)

# URL verification
if response_current.status_code == 200:
    data_current = response_current.json()

    # Current dataframe creation
    df_current = pd.DataFrame(data_current)
    # print(df_current.iloc[:, -1])

    # Associated CSV file creation
    df_current.to_csv("df_current.csv", index=False)

    # Current data extraction
    date_now = data_current["current"]["time"][:10]
    # print(date_now)
    temp_now = data_current["current"]["temperature_2m"]
    precip_now = data_current["current"]["precipitation"]
    wmo_now = data_current["current"]["weathercode"]
    wind_now = data_current["current"]["windspeed_10m"]
    wind_direc_now = data_current["current"]["winddirection_10m"]
    hour_now = data_current["current"]["time"][-5:]
else:
    print("Data retrieval error")

# We change "hour_now" because of the delay
h = hour_now
# We transform them in datetime object
heure_objet = datetime.strptime(h, "%H:%M")
# We add up 1 hour
nouvelle_heure = heure_objet + timedelta(hours=1)
# We convert the new hour in "hh:mm" format
hour_now_changed = nouvelle_heure.strftime("%H:%M")

# %%
"""
DATA DAILY
"""

# Daily data API extraction
url_daily = "https://api.open-meteo.com/v1/meteofrance?latitude=43.6109&longitude=3.8763&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_hours,winddirection_10m_dominant&timezone=Europe%2FLondon"
response_daily = requests.get(url_daily)

# Request verification
if response_daily.status_code == 200:
    data_daily = response_daily.json()
    # Daily dataframe creation
    df_daily = pd.DataFrame(data_daily)
    # print(df_daily.iloc[:, -1])
    pd.set_option("display.max_rows", None)

    # Associated CSV file creation
    df_daily.to_csv("df_daily.csv", index=False)

    # Daily data extraction
    tempmax = data_daily["daily"]["temperature_2m_max"]
    tempmin = data_daily["daily"]["temperature_2m_min"]
    wmo_daily = data_daily["daily"]["weathercode"]
    sunrise = data_daily["daily"]["sunrise"]
    sunset = data_daily["daily"]["sunset"]
    precip_daily_sum = data_daily["daily"]["precipitation_sum"]
    precip_hours_daily = data_daily["daily"]["precipitation_hours"]
    wind_direc_daily = data_daily["daily"]["winddirection_10m_dominant"]
else:
    print("Data retrieval error")


# Date initialization
Date = pd.to_datetime(data_daily["daily"]["time"])
Date = [datetime.strftime(a, "%A %d/%m") for a in Date]

# Hour modification sunrise and sunset
sunsetchanged = []
for i in range(len(df_daily["daily"]["sunset"])):
    # We take the sunset hours
    h = f'{df_daily["daily"]["sunset"][i][-5:]}'

    # We convert them in datetime object
    heure_objet = datetime.strptime(h, "%H:%M")

    # We add up 1 hour
    nouvelle_heure = heure_objet + timedelta(hours=1)

    # We transform the new hour in "hh:mm" format
    nouv_h_format = nouvelle_heure.strftime("%H:%M")

    # We put the changed hours in the list
    sunsetchanged.append(nouv_h_format)
sunrisechanged = []
for i in range(len(df_daily["daily"]["sunrise"])):
    # We take the sunrise hours
    h = f'{df_daily["daily"]["sunrise"][i][-5:]}'

    # We convert them in datetime object
    heure_objet = datetime.strptime(h, "%H:%M")

    # We add up 1 hour
    nouvelle_heure = heure_objet + timedelta(hours=1)

    # We transform the new hour in "hh:mm" format
    nouv_h_format = nouvelle_heure.strftime("%H:%M")

    # We put the changed hours in the list
    sunrisechanged.append(nouv_h_format)


# %%

"""
Hourly data
"""

# Hourly data API extraction
url_hourly = "https://api.open-meteo.com/v1/meteofrance?latitude=43.6109&longitude=3.8763&hourly=temperature_2m,windspeed_10m&timezone=Europe%2FLondon"
response_hourly = requests.get(url_hourly)

# URL verification
if response_hourly.status_code == 200:
    data_hourly = response_hourly.json()
    # Hourly dataframe creation
    df_hourly = pd.DataFrame(data_hourly)

    # Associated CSV file creation
    df_hourly.to_csv("df_hourly.csv", index=False)

    # Hourly data extraction
    temp_hourly = data_hourly["hourly"]["temperature_2m"]
    wind_hourly = data_hourly["hourly"]["windspeed_10m"]

    # We calculate the mean wind for the next 4 days
    size = 24
    # We create 4 sub-lists that each contains 24 different values (1 per hour)
    sub_lists = [
        wind_hourly[idx : idx + size] for idx in range(0, len(wind_hourly), size)
    ]

    # We create the function to calculate the mean of each sub-list
    def average_wind_daily():
        vent_moy = []
        for i in range(4):
            for j in sub_lists[i]:
                if j == None:
                    # We delete the "None" type objects elements from each sub-lists
                    del sub_lists[i][j]
            # We calculate the mean of each sub-list considering the changes if there was any None (len diminishes if that's the case)
            xmoy = sum(sub_lists[i]) / len(sub_lists[i])
            # We append each mean to a list that will contains all the means
            vent_moy.append(round(xmoy, 2))
        return vent_moy

    # Extraction of the hours (ignoring the date of the day)
    time_hourly = []
    for i in range(len(df_hourly["hourly"]["time"])):
        time_hourly.append(df_hourly["hourly"]["time"][i][-5:])
else:
    print("Data retrieval error")

vent_moy = average_wind_daily()  # List of the mean winds for the next 4 days

# %%
"""
HTML table of the CURRENT DATA
"""

tablenow = f"""
<table>
  <tr>
    <th style="text-align: center;"><strong>Date</strong></th>
    <th style="text-align: center;"><strong>WMO</strong></th>
    <th style="text-align: center;"><strong>Temperature</strong></th>
    <th style="text-align: center;"><strong>Precipitation</strong></th>
    <th style="text-align: center;"><strong>Wind</strong></th>
  </tr>
  <tr>
    <td style="text-align: center; vertical-align: middle;">{Date[0]}<br><strong>{hour_now_changed}</strong></td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_now)]['image']}><br>{descriptions[str(wmo_now)]['description']}</td>
    <td style="text-align: center; vertical-align: middle;">{temp_now} °C</td>
    <td style="text-align: center; vertical-align: middle;">{precip_now} mm</td>
    <td style="text-align: center; vertical-align: middle;">{wind_now} km/h
    <br>
    <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_now}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
  </tr>
</table>
"""

# HTML table rendering
HTML(tablenow)

# %%
"""
HTML table of DAILY FORECAST
"""

tabledaily = f"""
<table style="margin: 0 auto;">
  <tr>
    <th style ="background-color: rgb(240, 240, 240);"></th> 
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[0][:-5]}<br>{Date[0][-5:]}</th>
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[1][:-5]}<br>{Date[1][-5:]}</th>
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[2][:-5]}<br>{Date[2][-5:]}</th>
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[3][:-5]}<br>{Date[3][-5:]}</th>
  </tr>
    <td style="text-align: center;"><strong>WMO</strong></td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[0])]['image']}><br>{descriptions[str(wmo_daily[0])]['description']}</td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[1])]['image']}><br>{descriptions[str(wmo_daily[1])]['description']}</td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[2])]['image']}><br>{descriptions[str(wmo_daily[2])]['description']}</td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[3])]['image']}><br>{descriptions[str(wmo_daily[3])]['description']}</td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>Temperature</strong></td>
    <td style="text-align: center;">{tempmin[0]}°C-{tempmax[0]}°C</td>
    <td style="text-align: center;">{tempmin[1]}°C-{tempmax[1]}°C</td>
    <td style="text-align: center;">{tempmin[2]}°C-{tempmax[2]}°C</td>
    <td style="text-align: center;">{tempmin[3]}°C-{tempmax[3]}°C</td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>Precipitations</strong></td>
    <td style="text-align: center;">{precip_daily_sum[0]}mm<br><img src = "goutte.png"> {precip_hours_daily[0]}h</td>
    <td style="text-align: center;">{precip_daily_sum[1]}mm<br><img src = "goutte.png"> {precip_hours_daily[1]}h</td>
    <td style="text-align: center;">{precip_daily_sum[2]}mm<br><img src = "goutte.png"> {precip_hours_daily[2]}h</td>
    <td style="text-align: center;">{precip_daily_sum[3]}mm<br><img src = "goutte.png"> {precip_hours_daily[3]}h</td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>Wind</strong></td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[0]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[0]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[1]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[1]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[2]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[2]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[3]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[3]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>Sunrise/Sunset</strong></td>
    <td style="text-align: center;">{sunrisechanged[0]} - {sunsetchanged[0]}</td>
    <td style="text-align: center;">{sunrisechanged[1]} - {sunsetchanged[1]}</td>
    <td style="text-align: center;">{sunrisechanged[2]} - {sunsetchanged[2]}</td>
    <td style="text-align: center;">{sunrisechanged[3]} - {sunsetchanged[3]}</td>
  </tr>
</table>
"""

# HTML table rendering
HTML(tabledaily)

# %%
"""
ABOUT
"""
"""
Hourly data
"""

# Hourly data API extraction
url_hourly = "https://api.open-meteo.com/v1/forecast?latitude=43.6109&longitude=3.8763&hourly=temperature_2m,windspeed_10m&timezone=Europe%2FLondon"
response_hourly = requests.get(url_hourly)

# URL verification
if response_hourly.status_code == 200:
    data_hourly = response_hourly.json()
    # Hourly dataframe creation
    df_hourly = pd.DataFrame(data_hourly)

    # Associated CSV file creation
    df_hourly.to_csv("df_hourly.csv", index=False)

    # Hourly data extraction
    temp_hourly = data_hourly["hourly"]["temperature_2m"]
    wind_hourly = data_hourly["hourly"]["windspeed_10m"]

    # We calculate the mean wind for the next 7 days
    size = 24
    # We create 7 sub-lists that each contains 24 different values (1 per hour)
    sub_lists = [
        wind_hourly[idx : idx + size] for idx in range(0, len(wind_hourly), size)
    ]

    # We create the function to calculate the mean of each sub-list
    def average_wind_daily():
        vent_moy = []
        for i in range(7):
            for j in sub_lists[i]:
                if j == None:
                    # We delete the "None" type objects elements from each sub-lists
                    del sub_lists[i][j]
            # We calculate the mean of each sub-list considering the changes if there was any None (len diminishes if that's the case)
            xmoy = sum(sub_lists[i]) / len(sub_lists[i])
            # We append each mean to a list that will contains all the means
            vent_moy.append(round(xmoy, 2))
        return vent_moy

    # Extraction of the hours (ignoring the date of the day)
    time_hourly = []
    for i in range(len(df_hourly["hourly"]["time"])):
        time_hourly.append(df_hourly["hourly"]["time"][i][-5:])
else:
    print("Data retrieval error")

vent_moy = average_wind_daily()  # List of the mean winds for the next 7 days


"""
DATA DAILY
"""

# Daily data extraction
url_daily = "https://api.open-meteo.com/v1/forecast?latitude=43.6109&longitude=3.8763&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_hours,precipitation_probability_max,winddirection_10m_dominant&timezone=Europe%2FLondon"
response_daily = requests.get(url_daily)

# Request verification
if response_daily.status_code == 200:
    data_daily = response_daily.json()
    # Daily dataframe creation
    df_daily = pd.DataFrame(data_daily)
    # print(df_daily.iloc[:, -1])
    pd.set_option("display.max_rows", None)

    # Associated CSV file creation
    df_daily.to_csv("df_daily.csv", index=False)
    # Daily data extraction
    tempmax = data_daily["daily"]["temperature_2m_max"]
    tempmin = data_daily["daily"]["temperature_2m_min"]
    wmo_daily = data_daily["daily"]["weathercode"]
    sunrise = data_daily["daily"]["sunrise"]
    sunset = data_daily["daily"]["sunset"]
    uv = data_daily["daily"]["uv_index_max"]
    precip_daily_sum = data_daily["daily"]["precipitation_sum"]
    precip_proba_daily = data_daily["daily"]["precipitation_probability_max"]
    precip_hours_daily = data_daily["daily"]["precipitation_hours"]
    wind_direc_daily = data_daily["daily"]["winddirection_10m_dominant"]
else:
    print("Data retrieval error")


# Date initialization
Date = pd.to_datetime(data_daily["daily"]["time"])
Date = [datetime.strftime(a, "%A %d/%m") for a in Date]

# Hour modification sunrise and sunset
sunsetchanged = []
for i in range(len(df_daily["daily"]["sunset"])):
    # We take the sunset hours
    h = f'{df_daily["daily"]["sunset"][i][-5:]}'

    # We convert them in datetime object
    heure_objet = datetime.strptime(h, "%H:%M")

    # We add up 1 hour
    nouvelle_heure = heure_objet + timedelta(hours=1)

    # We transform the new hour in "hh:mm" format
    nouv_h_format = nouvelle_heure.strftime("%H:%M")

    # We put the changed hours in the list
    sunsetchanged.append(nouv_h_format)
sunrisechanged = []
for i in range(len(df_daily["daily"]["sunrise"])):
    # We take the sunrise hours
    h = f'{df_daily["daily"]["sunrise"][i][-5:]}'

    # We convert them in datetime object
    heure_objet = datetime.strptime(h, "%H:%M")

    # We add up 1 hour
    nouvelle_heure = heure_objet + timedelta(hours=1)

    # We transform the new hour in "hh:mm" format
    nouv_h_format = nouvelle_heure.strftime("%H:%M")

    # We put the changed hours in the list
    sunrisechanged.append(nouv_h_format)


# %%
"""
HTML table of DAILY FORECAST
"""

tabledaily = f"""
<table style="margin: 0 auto;">
  <tr>
    <th style ="background-color: rgb(240, 240, 240);"></th> <!-- Case vide -->
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[0]}</th>
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[1]}</th>
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[2]}</th>
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[3]}</th>
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[4]}</th>
    <th style="text-align: center;background-color: rgb(240, 240, 240); ">{Date[5]}</th>
  </tr>
    <td style="text-align: center;"><strong>WMO</strong></td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[0])]['image']}><br>{descriptions[str(wmo_daily[0])]['description']}</td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[1])]['image']}><br>{descriptions[str(wmo_daily[1])]['description']}</td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[2])]['image']}><br>{descriptions[str(wmo_daily[2])]['description']}</td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[3])]['image']}><br>{descriptions[str(wmo_daily[3])]['description']}</td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[4])]['image']}><br>{descriptions[str(wmo_daily[4])]['description']}</td>
    <td style="background-color: rgb(210,235,242); text-align: center;"><img src ={descriptions[str(wmo_daily[5])]['image']}><br>{descriptions[str(wmo_daily[5])]['description']}</td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>Temperature</strong></td>
    <td style="text-align: center;">{tempmin[0]}°C-{tempmax[0]}°C</td>
    <td style="text-align: center;">{tempmin[1]}°C-{tempmax[1]}°C</td>
    <td style="text-align: center;">{tempmin[2]}°C-{tempmax[2]}°C</td>
    <td style="text-align: center;">{tempmin[3]}°C-{tempmax[3]}°C</td>
    <td style="text-align: center;">{tempmin[4]}°C-{tempmax[4]}°C</td>
    <td style="text-align: center;">{tempmin[5]}°C-{tempmax[5]}°C</td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>UV</strong></td>
    <td style="text-align: center;">{uv[0]}</td>
    <td style="text-align: center;">{uv[1]}</td>
    <td style="text-align: center;">{uv[2]}</td>
    <td style="text-align: center;">{uv[3]}</td>
    <td style="text-align: center;">{uv[4]}</td>
    <td style="text-align: center;">{uv[5]}</td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>Precipitations</strong></td>
    <td style="text-align: center;">{precip_daily_sum[0]}mm<br><img src = "goutte.png"> {precip_proba_daily[0]}%</td>
    <td style="text-align: center;">{precip_daily_sum[1]}mm<br><img src = "goutte.png"> {precip_proba_daily[1]}%</td>
    <td style="text-align: center;">{precip_daily_sum[2]}mm<br><img src = "goutte.png"> {precip_proba_daily[2]}%</td>
    <td style="text-align: center;">{precip_daily_sum[3]}mm<br><img src = "goutte.png"> {precip_proba_daily[3]}%</td>
    <td style="text-align: center;">{precip_daily_sum[4]}mm<br><img src = "goutte.png"> {precip_proba_daily[4]}%</td>
    <td style="text-align: center;">{precip_daily_sum[5]}mm<br><img src = "goutte.png"> {precip_proba_daily[5]}%</td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>Wind</strong></td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[0]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[0]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[1]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[1]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[2]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[2]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[3]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[3]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[4]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[4]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
    <td style="text-align: center; vertical-align: middle; ">
      {vent_moy[5]}km/h
      <br>
      <div style="width: 20px; height: 20px; overflow: hidden; transform: rotate({wind_direc_daily[5]}deg); display: inline-block; margin: 0 auto;">
        <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 15px solid black;">
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td style="text-align: center;"><strong>Sunrise/Sunset</strong></td>
    <td style="text-align: center;">{sunrisechanged[0]} - {sunsetchanged[0]}</td>
    <td style="text-align: center;">{sunrisechanged[1]} - {sunsetchanged[1]}</td>
    <td style="text-align: center;">{sunrisechanged[2]} - {sunsetchanged[2]}</td>
    <td style="text-align: center;">{sunrisechanged[3]} - {sunsetchanged[3]}</td>
    <td style="text-align: center;">{sunrisechanged[4]} - {sunsetchanged[4]}</td>
    <td style="text-align: center;">{sunrisechanged[5]} - {sunsetchanged[5]}</td>
  </tr>
</table>
"""

# HTML table rendering
HTML(tabledaily)


# %%
# Essai de filtre pour None type objects

x = None
lis = [x, 2]
lis = [i for i in lis if i is not None]
print(lis)

x = None
l = [x, 2]
clean = list(filter(lambda x: x is not None, l))
print(clean)

l = [x, 2]
while None in lis:
    lis.remove(None)
print(lis)

# %%

start_date = str(date.today())
print(start_date)


descriptions[str(wmo_daily[2])]["description"] = "- "
descriptions[str(wmo_daily[2])]["image"] = "- "
print(descriptions[str(wmo_daily[2])]["image"])

table = f"""
<table>
  <tr>
    <th>test</th>
  </tr>
  <tr>
    <td><img src ={descriptions[str(wmo_daily[1])]['image']}></td>
  </tr>
</table>
"""
HTML(table)
