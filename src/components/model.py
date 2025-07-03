import os
import sys
import joblib
import pandas as pd
from src.config import CONFIG
from src.logger import logging
from src.exception import MyException
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

class ModelTraining:

    def __init__(self):
        """Initialize the data ingestion class."""
        self.config = CONFIG["model_training"]
        logging.info("Model training class initialized.")

    def handle_training(self, X_train, X_test, y_train, y_test) -> None:

        try:
            # Define preprocessing steps
            column_trans = make_column_transformer(
                (OneHotEncoder(sparse_output=False), ['location']),
                remainder='passthrough'
            )
            scaler = StandardScaler()

            # Define models
            models = {
                'lr': LinearRegression(), 
                'lasso': Lasso(),
                'ridge': Ridge(),
            }

            best_model_name = None
            best_model_pipeline = None
            best_score = float('-inf')

            # Try each model with full pipeline
            for name, model in models.items():
                pipeline = make_pipeline(column_trans, scaler, model)
                pipeline.fit(X_train, y_train)
                
                y_pred = pipeline.predict(X_test)
                score = r2_score(y_test, y_pred)

                print(f"{name} with R2 score: {score:.4f}")

                if score > best_score:
                    best_score = score
                    best_model_name = name
                    best_model_pipeline = pipeline

            # Final output
            print(f"\nBest model: {best_model_name} with R2 score: {best_score:.4f}")


            # Save the best pipeline (preprocessing + model)
            model_path = self.config["model"]
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            joblib.dump(best_model_pipeline, open(model_path, 'wb'))

            return

        except Exception as e:
            logging.error("Error occurred while extracting zip file", exc_info=True)
            raise MyException(e, sys)

