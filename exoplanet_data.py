import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from math import *
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchiveClass

nasa = NasaExoplanetArchiveClass()

planets = nasa.query_criteria(table="pscomppars", select="pl_name, pl_rade, pl_masse, pl_dens, pl_orbper, pl_orbsmax, pl_insol, pl_eqt, st_teff, st_mass, st_rad, st_age, st_met, st_lum",
                              cache=False)
exoDF = planets.to_pandas()
scoredict = {}
parameters = {"Mass": 0, "Radius": 0, "Temp": 0, "Density": 0, "Zone": 0, "4+ Met": 0}

for index, row in exoDF.iterrows():
    score = 0
    name = row["pl_name"]
    radius = row["pl_rade"] # earth radii
    mass = row["pl_masse"] # earth mass
    density = row["pl_dens"] # g/cm^3
    temp = row["pl_eqt"] # K
    orbsmax = row["pl_orbsmax"] # AU

    if pd.isna(mass) or pd.isna(radius) or pd.isna(density) or pd.isna(temp) or pd.isna(orbsmax) or pd.isna(row["st_lum"]):
        continue

    lum = 10 ** row["st_lum"]

    rinner = sqrt(lum / 1.1) # AU
    router = sqrt(lum / 0.53) # AU

    if 0.5 <= mass <= 2: # check if mass is earthlike
        score += 1
        parameters["Mass"] += 1
    if 0.5 <= radius <= 1.5: # check if radius is earthlike
        score += 1
        parameters["Radius"] += 1
    if 273 <= temp <= 323: # check if temp is between 0 C and 50 C
        score += 1
        parameters["Temp"] += 1
    if 4.5 <= density <= 6: # check if density is rocky planet like
        score += 1
        parameters["Density"] += 1
    if rinner <= orbsmax <= router: # check if planet is within goldilocks zone
        score += 1
        parameters["Zone"] += 1
    if score >= 3:
        parameters["3+ Met"] += 1
        print(name)
        print(mass)
        print(radius)
        print(temp)
        print(density)
        print(f"{rinner} {orbsmax} {router}") 
    scoredict[name] = score

score_series = pd.Series(scoredict)
parameter_series = pd.Series(parameters)

sns.barplot(x=parameter_series.index, y=parameter_series.values, palette="viridis")
plt.title('Times Habitability Conditions Met')
plt.xlabel('Condition')
plt.ylabel('Count of Conditions Met')
plt.show()