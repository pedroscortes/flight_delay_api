import pandas as pd
import numpy as np
from typing import Tuple, Union, List
from sklearn.linear_model import LogisticRegression
from datetime import datetime

class DelayModel:
    def __init__(
        self
    ):
        self._model = None
        self._features = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.
        """
        data = data.copy()  
        
        def get_min_diff(row):
            fecha_o = datetime.strptime(row['Fecha-O'], '%Y-%m-%d %H:%M:%S')
            fecha_i = datetime.strptime(row['Fecha-I'], '%Y-%m-%d %H:%M:%S')
            min_diff = ((fecha_o - fecha_i).total_seconds())/60
            return min_diff

        data['min_diff'] = data.apply(get_min_diff, axis=1)
        data['delay'] = (data['min_diff'] > 15).astype(int)

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)
        
        features = features.reindex(columns=self._features, fill_value=0)
        
        if target_column:
            target = pd.DataFrame(data['delay'])
            return features, target
        
        return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.
        """
        n_y0 = len(target[target['delay'] == 0])
        n_y1 = len(target[target['delay'] == 1])
        
        self._model = LogisticRegression(
            class_weight={
                1: n_y0/len(target), 
                0: n_y1/len(target)
            }
        )
        self._model.fit(features, target['delay'])

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.
        """
        if self._model is None:
            raise ValueError("Model not trained. Call fit() first.")
        
        predictions = self._model.predict(features)
        return predictions.tolist()
