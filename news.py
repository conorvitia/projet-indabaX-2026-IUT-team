import pandas as pd 
import numpy as np 
import matplotlib as plt 
import seaborn as sns 


#chargement du dataset initial 
try:
    df = pd.read_excel('../data/Dataset_complet_Meteo.xlsx')
    #print(df.head())
    num_cols= [
    'temperature_2m_max', 'temperature_2m_min', 'temperature_2m_mean',
    'apparent_temperature_mean', 'precipitation_sum', 'rain_sum',
    'wind_speed_10m_max', 'wind_gusts_10m_max',
    'shortwave_radiation_sum', 'et0_fao_evapotranspiration',
    'sunshine_duration', 'latitude', 'longitude', 'daylight_duration'
    ]
    for cols in num_cols:
        df[cols] = pd.to_numeric(df[cols],errors='coerce')    
    #gestion du temps 
    #convertissons la colone time en format date
    date_jour = ['time']
    for date in date_jour:
        df[date] = pd.to_datetime(df[date],errors='coerce')
    #trions le dataset en ville ,puis par date 
    df_propre = df.sort_values(['city','time']).copy()
    #print(df_propre)
    #a présent enlevons les valeurs manquantes 
    
    # On remplit vers le bas, PUIS vers le haut, le tout groupé par ville
    df_propre = df_propre.groupby('city').apply(lambda x: x.ffill().bfill(), include_groups=False).reset_index()

    #on reset l'index 
    
    print(f"le reste des valeurs manquante est {df_propre.isnull().sum()}")   
   
    #passons au feature engineering
    df_propre['temp_hier'] = df_propre.groupby('city')['temperature_2m_mean'].shift(1)
    print(df_propre['temp_hier'].head())
    
    #df_propre['pollution_hier'] = df_propre.groupby('city')[''].shift(1)
    
except  Exception as e :
    print(f"Erreur à ce niveau {e}")