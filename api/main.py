from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import xgboost as xgb


app = FastAPI()

class Request(BaseModel):
    grid: int
    constructor:int
    race:int
    driver:int

@app.post("/predict")
def predict(req:Request):
    pd.options.mode.chained_assignment = None  # default='warn'
    data_df = pd.read_csv('results.csv')
    cols_to_keep = ['raceId', 'driverId', 'constructorId', 'grid','positionOrder']
    df = data_df[cols_to_keep]

    #On choisit les colonnes raceId, driverId et grid pour créer une nouvelle colonne moy_grid_by_race
    moy_grid_race = data_df[["raceId","driverId","grid"]]

    # On calcule la moyenne de grid par driver et race
    def calculate_mean_grid_race(line):
        raceID = line["raceId"]
        driveID = line["driverId"]
        mean_grid = moy_grid_race.loc[(df["driverId"] == driveID) & (df["raceId"] == raceID), "grid"].mean()
        return mean_grid
    
    #  et on l'ajoute à notre array principal
    df["moy_grid_by_race"] = df.apply(calculate_mean_grid_race, axis = 1)


    # on repete l'opération d'avant mais cette fois avec le constructor à la place du driver

    moy_grid_constructor = data_df[["raceId","constructorId","grid"]]
    def calculate_mean_grid_constructor(line):
        constructorID = line["constructorId"]
        driveID = line["driverId"]
        mean_grid = moy_grid_constructor.loc[(df["driverId"] == driveID) & (df["constructorId"] == constructorID), "grid"].mean()
        return mean_grid
    
    df["moy_grid_by_constructor"] = df.apply(calculate_mean_grid_constructor, axis = 1)

    # on vectorise les constructeurs

    vectorizer = CountVectorizer()
    constructor_ids = df['constructorId'].astype(str).values.tolist()
    vectorized_constructor_ids = vectorizer.fit_transform(constructor_ids)
    constructor_id_vectors = vectorized_constructor_ids.toarray()
    constructor_id_df = pd.DataFrame(constructor_id_vectors)
    constructor_id_df = constructor_id_df.add_prefix('constructor_')
    df = pd.concat([df, constructor_id_df], axis=1)

    #On vectorise les drivers
    vectorizer = CountVectorizer()
    driver_ids = df['driverId'].astype(str).values.tolist()
    vectorized_driver_ids = vectorizer.fit_transform(driver_ids)
    driver_id_vectors = vectorized_driver_ids.toarray()
    driver_id_df = pd.DataFrame(driver_id_vectors)
    driver_id_df = driver_id_df.add_prefix('driver_')
    df = pd.concat([df, driver_id_df], axis=1)


    # On charge le model précédement entrainer avec jupyter
    saved_model = xgb.Booster()
    saved_model.load_model('xgb_model.model')

    mean_grid_race = df.loc[(df["driverId"] == req.driver) & (df["raceId"] == req.race), "grid"].mean()
    mean_grid_constructor = df.loc[(df["driverId"] == req.driver) & (df["constructorId"] == req.constructor) , "grid"].mean()

    print('MEAN',req.race,mean_grid_constructor,mean_grid_race)

    # On crée la ligne de test
    test_data = {
        'raceId': [req.race],
        'driverId': [req.driver],
        'constructorId': [req.constructor],
        'grid': [req.grid],
        'moy_grid_by_race': [mean_grid_race],
        'moy_grid_by_constructor': [mean_grid_constructor]
    }
    
    test_df = pd.DataFrame(data=test_data)
    test_df['constructorId'] = test_df['constructorId'].astype(str)
    test_df['driverId'] = test_df['driverId'].astype(str)

    # On récupère les colonnes vectorisées correspondant au driver et au constructeur dans df
    driver_cols = [col for col in df.columns if col.startswith('driver_')]
    constructor_cols = [col for col in df.columns if col.startswith('constructor_')]

    # On ajoute les colonnes vectorisées correspondant au driver et au constructeur dans la ligne de test
    for col in driver_cols:
        test_df[col] = 0
        if 'driver_' + test_df['driverId'][0] in col:
            test_df[col] = 1

    for col in constructor_cols:
        test_df[col] = 0
        if 'constructor_' + test_df['constructorId'][0] in col:
            test_df[col] = 1

    # On supprime les colonnes driverId et constructorId qui ne sont plus nécessaires
    test_df.drop(['driverId', 'constructorId'], axis=1, inplace=True)

    # On utilise le modèle pour faire une prédiction
    y_pred = saved_model.predict(xgb.DMatrix(test_df))
    print('get',req.grid,y_pred)
    return y_pred.tolist()



# uvicorn main:app --reload --port 7999 
# python3 -m uvicorn main:app --reload --port 7999 