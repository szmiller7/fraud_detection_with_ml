import sys
from src.exception import CustomException
import os 
from dataclasses import dataclass
import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from data_config import transaction_cols, num_cols, cat_cols_fillna_unknown, cols_browser_recategorize, cols_domain_recategorize, cols_toDummyConvert
from src.logger import logging


@dataclass
class DataPreparationConfig:
    """Specify inputs"""
    preprocessed_train_data_file_path = os.path.join("fraud_data","train_preprocessed.csv")
    preprocessed_test_data_file_path = os.path.join("fraud_data","test_preprocessed.csv")
    

class DataPreparation:
    def __init__(self):
        self.data_preparation_config =  DataPreparationConfig()

    def initiate_data_preparation(self, raw_data_path, na_perc_drop=0.1):
        try:
            
            df = pd.read_csv(raw_data_path)
            logging.info("Read dataset")

            logging.info("Starting data preparation")

            # remove variables with over X% of missing values
            columns_na_perc = df.isnull().mean() 
            na_id_drop = columns_na_perc[columns_na_perc<=na_perc_drop].index
            df = df[na_id_drop]
            logging.info(f"Dropped columns with more than {100*na_perc_drop}% missing values")

            # drop transaction id and dt
            for col in transaction_cols:
                if col in df.columns:
                    df = df.drop(columns=col)
            logging.info(f"Dropped transaction cols {transaction_cols}")

            # replace missing values with unknown
            for col in cat_cols_fillna_unknown:
                if col in df.columns:
                    df.loc[:,[col]] = df.loc[:,[col]].fillna("Unknown")
            logging.info("Replaced missing values with unknown")

            # perform recategorization
            for col in cols_browser_recategorize:
                if col in df.columns:
                    df[col] = df[col].astype(str).apply(browser_recategorization)
            for col in cols_domain_recategorize:
                if col in df.columns:
                    df[col] = df[col].astype(str).apply(emaildomain_recategorization)
            logging.info("Performed recategorisation")

            # drop unary variables
            unary_val_columns = [col for col in df.columns if df[col].nunique == 1]
            df = df.drop(unary_val_columns, axis=1) 
            logging.info("Dropped unary variables")

            # drop rows with no value of Y
            missing_y = df['isFraud'].isna().sum()
            df = df.dropna(subset=['isFraud'])
            logging.info(f"{missing_y} rows dropped due to no label value")

            # Partition data
            X = df.drop('isFraud', axis=1)
            y = df['isFraud']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, stratify=y, random_state=100)
            logging.info('Partitioned data')

            # store only variables that were not excluded in the missing value per column analysis
            cat_cols_current = list(set(X.columns) - set(num_cols))
            num_cols_current = list(set(X.columns) - set(cat_cols_current))
            logging.info("Updated lists of included columns")

            ########### Impute missing values

            # numerical predictors imputation
            imp_mean = SimpleImputer(strategy='mean')
            imp_mean = imp_mean.fit(X_train[num_cols_current])
            X_train[num_cols_current] = imp_mean.transform(X_train[num_cols_current])
            X_test[num_cols_current] = imp_mean.transform(X_test[num_cols_current])
            logging.info('Imputed numercial variables')

            # categorical/ordinal predictors imputation
            imp_mode = SimpleImputer(strategy='most_frequent')
            imp_mode = imp_mode.fit(X_train[cat_cols_current])
            X_train[cat_cols_current] = imp_mode.transform(X_train[cat_cols_current])
            X_test[cat_cols_current] = imp_mode.transform(X_test[cat_cols_current])
            logging.info('Imputed categorical variables')

            X_train, X_test = ohe(X_train, X_test, cols_toDummyConvert)
            logging.info("Performed OHE")

            # merge into train and test set
            df_train = pd.concat([X_train, y_train], axis=1)
            df_test = pd.concat([X_test, y_test], axis=1)
            logging.info("Merged into train and test dfs")

            # save data 
            df_train.to_csv(self.data_preparation_config.preprocessed_train_data_file_path,index=False)
            df_test.to_csv(self.data_preparation_config.preprocessed_test_data_file_path,index=False)
            logging.info("Saved train and test sets")
            
            return (self.data_preparation_config.preprocessed_train_data_file_path, self.data_preparation_config.preprocessed_test_data_file_path)

        except Exception as e:
            raise CustomException(e, sys)


def browser_recategorization(row):
    """
    Browser recategorization function
    """
    browser_categories = ["chrome", "safari", "edge", "firefox", "samsung", "opera"]
    row_lower = row.lower()
    for category in browser_categories:
        if category in row_lower:
            return category
    return "other"


def emaildomain_recategorization(row):
    """
    email domain recategorization function
    """
    domain_categories = ["gmail", "hotmail", "yahoo", "anonymous", "aol", "outlook", "comcast", "icloud"]
    row_lower = row.lower()
    for category in domain_categories:
        if category in row_lower:
            return category
    return "other"

def ohe(X_train, X_test, cols_toDummyConvert):

    # Instantiate the OneHotEncoder with handle_unknown='ignore'
    encoder = OneHotEncoder(handle_unknown='ignore')
    # Fit the encoder on the training data and transform both the training and test data
    X_train_encoded = encoder.fit_transform(X_train[cols_toDummyConvert])
    X_test_encoded = encoder.transform(X_test[cols_toDummyConvert])
    # Convert the encoded data back to DataFrames
    X_train_encoded = pd.DataFrame(X_train_encoded.toarray(), columns=encoder.get_feature_names_out(cols_toDummyConvert), index=X_train.index)
    X_test_encoded = pd.DataFrame(X_test_encoded.toarray(), columns=encoder.get_feature_names_out(cols_toDummyConvert), index=X_test.index)
    # Concatenate the encoded data with the original data, and drop the original columns
    X_train = pd.concat([X_train, X_train_encoded], axis=1).drop(columns=cols_toDummyConvert)
    X_test = pd.concat([X_test, X_test_encoded], axis=1).drop(columns=cols_toDummyConvert)

    return X_train, X_test



if __name__ == "__main__":
    obj = DataPreparation()
    obj.initiate_data_preparation(raw_data_path='fraud_data/raw.csv')
