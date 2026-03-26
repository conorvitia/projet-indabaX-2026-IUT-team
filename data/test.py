import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#chargement du dataset 
df = pd.read_excel('../data/Dataset_complet_Meteo.xlsx')
#conversion des colones numériques stocké en string dans le fichier
num_cols = [
    'temperature_2m_max', 'temperature_2m_min', 'temperature_2m_mean',
    'apparent_temperature_mean', 'precipitation_sum', 'rain_sum',
    'wind_speed_10m_max', 'wind_gusts_10m_max',
    'shortwave_radiation_sum', 'et0_fao_evapotranspiration',
    'sunshine_duration', 'latitude', 'longitude'
]
for col in num_cols :
    df[col]= pd.to_numeric(df[col], errors='coerce')
print(f"Dataset : {df.shape[0]:,} obs × {df.shape[1]} variables")
print(f"   Période  : {df['time'].min().date()} → {df['time'].max().date()}")
print(f"   Villes   : {df['city'].nunique()} | Régions : {df['region'].nunique()}")
df.head(3)