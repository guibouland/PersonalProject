# Weather in Montpellier
Please visit our [website](https://guibouland.github.io/PersonalProject/) to know more about the project.

The project's main goal was to develop a website using Quarto that would display the weather forecast for the next 4 days in Montpellier.

## Project Description
### What does it do?
Our website displays two types of tables using HTML in a python cell with the *IPython.display* module:
- **Now :** A table that displays the current weather (updated every hour) with the following parameters:  
    - *Date* and *hour* when the data was measured,  
    - An image and a description corresponding to its *WMO code* (World Meteorological Organization) : we used a [JSON](descriptions.json) file to get all the URLs and descriptions of all the WMO codes,  
    - *Temperature* (in °C),  
    - *Precipitations :* the amount of precipitation (in mm),  
    - *Wind* (in km/h) and its *direction* (with an arrow).  
- **Forecast :** A table displaying the weather for the next 4 days, with all the parameters listed above and a few extras:  
    - *Temperature :* the minimum and the maximum of the day,  
    - *Precipitations :* the amount mentioned above but also the number of hours of precipitation,  
    - *Wind :* Here, the wind is given with its average value of the day, we had to get the hourly data and calculate the mean of each day,
    - *Sunrise/Sunset :* the hour when the Sun rises and sets each day.  

> potential plot

### Technologies used
The entirety of this project was coded in Python, with modules you can find in the [requirements.txt](requirements.txt) file (Pandas, Numpy, ...), but also with other built-in modules :  
- *Datetime :* Used to change the hours due to a delay,
- *Requests :* Used to request the various URLs,
- *Pandas :* Used to create the data frames with the data contained in the URLs,
- *Csv :* To convert the data frames in csv files,
- *Json :* Used to open and reference the [JSON](descriptions.json) file mentioned previously,
- *IPython.display :* To display the HTML tables in Quarto Markdown.

### Challenges and Upgrades
During the development phase of this project, we faced a fex issues.  

We were somewhat limited regarding the API.  MeteoFrance did not have all the parameters we needed, such as the precipitation probability or UV index, which were found in other forecast data sources (with differences in measurements). The length of the forecast was also a bit short compared to the others that could go to over a week.

Also, we struggled to come up with a viable solution to display a table coded in a Python cell that could display the images using an URL in Quarto. This resulted in us learning how to create HTML tables with CSS styling (which was beneficial in many ways).

A major problem arose when data was missing because of lack of measurement, thus all of the automatic Quarto publishing was doomed because it could not do operations with None type objects, we had to modify the data when that occurs.

We can, then, wish an improvement in the MeteoFrance API in order to have more daily parameters and an extended forecast length.

## How to use our Website
This website contains two main pages. The first one, **Home**, contains an HTML table of the current weather and an HTML table of the forecasted weather for the next 4 days. The second page, **Learn more**, contains an HTML table which doesn't use the MeteoFrance data but generic data that the [website](https://open-meteo.com/en/docs) contains, it shows the forecast for the next 6 days in Montpellier. It also includes a brief description of the methodology used.

## Credits
The purpose of this website was not to be used for commercial purposes, as per the following [terms](https://open-meteo.com/en/terms).

In order to display the corresponding images depending on the WMO codes, we used a JSON file that we modified which was found [here](https://gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c).