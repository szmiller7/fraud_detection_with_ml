import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from data_config import transaction_cols

@dataclass
class DataReaderConfig:
    train_data_path :str = os.path.join('fraud_data',"train.csv")
    test_data_path :str = os.path.join('fraud_data',"test.csv")
    raw_data_path :str = os.path.join('fraud_data',"raw.csv")

class DataReader:
    def __init__(self):
        # save paths 
        self.reader_config = DataReaderConfig()

    def initiate_data_reader(self, na_perc_drop=0.1):
        logging.info("Entered the data reading module")
        try:
            # read data
            df_trans = pd.read_csv("data/train_transaction.csv")
            df_id = pd.read_csv("data/train_identity.csv")
            logging.info("Loaded identify and transactional data")

            # keep only those transactions that have identity info 
            df = pd.merge(df_trans, df_id, how="inner", on = "TransactionID")
            logging.info("Merged datasets")

            # remove variables with over X% of missing values
            columns_na_perc = df.isnull().mean() 
            na_id_drop = columns_na_perc[columns_na_perc<=na_perc_drop].index
            df = df[na_id_drop]
            logging.info(f"Dropped columns with more than {100*na_perc_drop}% missing values")

            # drop transaction id and dt
            df = df.drop(transaction_cols, axis=1)
            logging.info(f"Dropped transaction cols {transaction_cols}")
            
            # create directory for data save
            os.makedirs(os.path.dirname(self.reader_config.train_data_path), exist_ok=True)
            # save raw data
            df.to_csv(self.reader_config.raw_data_path,index=False)
            # split and save train, test data
            logging.info("Initiated train test split")
            train_set, test_set = train_test_split(df, test_size=0.3, random_state=100)
            train_set.to_csv(self.reader_config.train_data_path, index=False)
            test_set.to_csv(self.reader_config.test_data_path ,index=False)
            logging.info("Completed data reading")

            return ( 
                self.reader_config.train_data_path,
                self.reader_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)
            
    
if __name__ == "__main__":
    obj = DataReader()
    obj.initiate_data_reader()
    

