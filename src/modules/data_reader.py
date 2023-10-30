import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass
class DataReaderConfig:
    raw_data_path :str = os.path.join('fraud_data',"raw.csv")

class DataReader:
    def __init__(self):
        # save paths 
        self.reader_config = DataReaderConfig()

    def initiate_data_reader(self):
        logging.info("Entered the data reading module")
        try:
            # read data
            df_trans = pd.read_csv("data/train_transaction.csv")
            df_id = pd.read_csv("data/train_identity.csv")
            logging.info("Loaded identify and transactional data")

            # keep only those transactions that have identity info 
            df = pd.merge(df_trans, df_id, how="inner", on = "TransactionID")
            logging.info("Merged datasets")
            
            # create directory for data save
            os.makedirs(os.path.dirname(self.reader_config.raw_data_path), exist_ok=True)
            # save raw data
            df.to_csv(self.reader_config.raw_data_path,index=False)
            logging.info("Saved data - COMPLETED DATA READING")

            return (self.reader_config.raw_data_path)

        except Exception as e:
            raise CustomException(e, sys)
            
    
if __name__ == "__main__":
    obj = DataReader()
    obj.initiate_data_reader()
    

