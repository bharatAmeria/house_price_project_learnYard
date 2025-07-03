import os
import sys
import numpy as np
import pandas as pd
from src.config import CONFIG
from src.logger import logging
from src.exception import MyException
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class DataPreprocess:
    """
    Data preprocessing strategy which preprocesses the data.
    """

    def __init__(self):
        """Initialize the data ingestion class."""
        self.config = CONFIG["data_ingest"]
        self.df = None
        logging.info("Data Processing class initialized.")


    def handle_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes columns which are not required, fills missing values with median average values,
        and converts the data type to float.
        """
        try:

            logging.info(f"Dataset shape before processing: {df.shape}")
            logging.info(f"Dataset Info before processing: {df.info()}")

            df.drop(columns=['area_type', 'availability', 'society', 'balcony'], inplace=True)

            df['location'] = df['location'].fillna('Sarjapur Road')

            df['size'] = df['size'].fillna('2 BHK')

            df['bath'] = df['bath'].fillna(df['bath'].median())

            df['bhk'] = df['size'].str.split().str.get(0).astype(int)

            df['total_sqft'] = df['total_sqft'].apply(self.convertRange)

            #  Price per sqft
            df['price_per_sqft'] = df['price']*100000/df['total_sqft']

            df['location'] = df['location'].apply(lambda x: x.strip())
            location_count = df['location'].value_counts()
            location_count_less_10 = location_count[location_count <=10]
            df['location'] = df['location'].apply(lambda x: 'other' if x in location_count_less_10 else x)

            # Outlier Detection and Removal

            df = df[((df['total_sqft']/df['bhk']) >= 300)]

            df = self.remove_outliers_sqft(df)

            df = self.bhk_outlier_remover(df)

            df.drop(columns=['size', 'price_per_sqft'], inplace=True)

            save_path = CONFIG["processed_data_path"]
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df.to_csv(save_path, index=False)
            logging.info(f"Successfully saved processed data to {save_path}")

            self.df = df
            
            return df

        except Exception as e:
            logging.error("Error occurred in Processing data", exc_info=True)
            raise MyException(e, sys)
        
    def bhk_outlier_remover(self, df):
        exclude_indices = np.array([])
        for location, location_df in df.groupby('location'):
            bhk_stats = {}
            for bhk, bhk_df in location_df.groupby('bhk'):
                bhk_stats[bhk] = {
                    'mean' : np.mean(bhk_df.price_per_sqft),
                    'std' : np.std(bhk_df.price_per_sqft),
                    'count' : bhk_df.shape[0]
                }

            for bhk, bhk_df in location_df.groupby('bhk'):
                stats = bhk_stats.get(bhk - 1)
                if stats and stats['count'] > 5:
                    exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft < (stats['mean'])].index.values)
        
        return df.drop(exclude_indices, axis='index')


        
    def remove_outliers_sqft(self, df):
        df_output = pd.DataFrame()
        for key, subdf in df.groupby('location'):
            m = np.mean(subdf.price_per_sqft)

            st = np.std(subdf.price_per_sqft)

            gen_df = subdf[(subdf.price_per_sqft > (m-st)) & (subdf.price_per_sqft <= (m+st))]
            df_output = pd.concat([df_output, gen_df], ignore_index=True)

        return df_output
    
    def convertRange(self, x):
        temp = x.split('-')
        if len(temp) == 2:
            return (float(temp[0]) + float(temp[1]))/2
        try:
            return float(x)
        except:
            return None
        
    def split_data_as_train_test(self) -> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            if self.df is None:
                raise ValueError("Data must be processed first using `handle_data()` before splitting.")

            X = self.df.drop(columns = ['price'])
            y = self.df['price']
            train_set, test_set, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")

            dir_path = os.path.dirname(self.config["FILE_NAME"])
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            os.makedirs(os.path.dirname(self.config["TRAIN_FILE_NAME"]), exist_ok=True)
            pd.DataFrame(train_set).to_csv(self.config["TRAIN_FILE_NAME"], index=False)
            pd.DataFrame(test_set).to_csv(self.config["TEST_FILE_NAME"], index=False, header=True)
            pd.DataFrame(y_train).to_csv(self.config["TRAIN_LABEL_FILE_NAME"], index=False)
            pd.DataFrame(y_test).to_csv(self.config["TEST_LABEL_FILE_NAME"], index=False)

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise MyException(e, sys)
        
