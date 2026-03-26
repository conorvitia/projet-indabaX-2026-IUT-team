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
    
    df_propre['pm25_proxy'] = (0.3 * df_propre['temperature_2m_mean'] + 
                           0.2 * df_propre['shortwave_radiation_sum']).clip(lower=0)
    #passons au feature engineering
    
    # 2. MÉMOIRE (Shift) (les lags)
    df_propre['pollution_hier'] = df_propre.groupby('city')['pm25_proxy'].shift(1)
    #enlevons les nan sur la colonne
    df_propre['pollution_hier']=df_propre.groupby('city')['pollution_hier'].transform(lambda x: x.ffill().bfill())
    
    df_propre['temp_hier'] = df_propre.groupby('city')['temperature_2m_mean'].shift(1)
    #tendance sur les 3 dernirs jours
    df_propre['moyenne_mobile_3j'] = df_propre.groupby('city')['pm25_proxy'].transform(lambda x: x.rolling(window=3).mean())
    # 4. ANOMALIE (Ecart à la moyenne de la ville)
    moyenne_par_ville = df_propre.groupby('city')['temperature_2m_max'].transform('mean')
    df_propre['temp_anomalie'] = df_propre['temperature_2m_max'] - moyenne_par_ville
    
    print("Feature Engineering terminé avec succès !")
    print(df_propre[['city', 'time', 'pm25_proxy', 'pollution_hier', 'temp_anomalie']].head())
    
except  Exception as e :
    print(f"Erreur à ce niveau {e}")
    
    
 





