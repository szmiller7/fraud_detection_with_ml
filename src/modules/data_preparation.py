import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd 
from data_config import outcome_cols, transaction_cols, cat_cols, num_cols, cat_cols_fillna_unknown, cols_browser_recategorize, cols_domain_recategorize
from src.logger import logging


@dataclass
class DataPreparationConfig:
    """Specify inputs"""
    preprocessed_data_file_path = os.path.join("fraud_data","preprocessed_data.pkl")

class DataPreparation:
    def __init__(self):
        self.data_preparation_config =  DataPreparationConfig()


    def initiate_data_preparation(self, train_path, test_path):
        try:
            train_set = pd.read_csv(train_path)
            test_set = pd.read_csv(test_path)
            logging.info("Read train and test set")

            logging.info("Starting data preparation")

            # store only variables that were not excluded in the missing value per column analysis
            outcome_cols_remNA = list(set(outcome_cols).intersection(df.columns))
            transaction_cols_remNA = list(set(transaction_cols).intersection(df.columns))
            cat_cols_remNA = list(set(cat_cols).intersection(df.columns))
            num_cols_remNA = list(set(num_cols).intersection(df.columns))
            logging.info("Group relevant columns based on type")

            # replace missing values with unknown
            df.loc[:,[cat_cols_fillna_unknown]] = df.loc[:,[cat_cols_fillna_unknown]].fillna("Unknown")

            # perform recategorization
            for col in cols_browser_recategorize:
                df[col] = df[col].astype(str).apply(browser_recategorization)
            for col in cols_domain_recategorize:
                df[col] = df[col].astype(str).apply(emaildomain_recategorization)

            # drop unary variables
            unary_val_columns = [col for col in df.columns if df[col].nunique == 1]
            df = df.drop(unary_val_columns, axis=1) 

            ############## rethink this
            # categorical columns to impute with mode
            cat_cols_remNA_toImpute = list(set(X.columns) - set(num_cols_remNA))
            # numerical columns to impute with average
            num_cols_remNA = list(set(num_cols_remNA) - set(unary_variables))

        except:
            pass



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

################### recategosie email domain columns


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