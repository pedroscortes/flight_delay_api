import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple, Union, List
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

class DelayModel:
    def __init__(self):
        self._model = None
        self._scaler = None
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
        
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)
        
        features = features.reindex(columns=self._features, fill_value=0)

        if self._scaler is not None:
            features = pd.DataFrame(
                self._scaler.transform(features),
                columns=features.columns
            )
        
        return features

    def fit(
            self,
            features: pd.DataFrame,
            target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.
        """
        self._scaler = StandardScaler()
        features_scaled = self._scaler.fit_transform(features)
        
        self._model = LogisticRegression(random_state=42)
        self._model.fit(features_scaled, target['delay'].values)

    def predict(
            self,
            features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.
        """
        if self._model is None:
            raise ValueError("Model not trained. Call fit() first.")
        
        if self._scaler is not None:
            features = self._scaler.transform(features)
        
        predictions = self._model.predict(features)
        return predictions.tolist()