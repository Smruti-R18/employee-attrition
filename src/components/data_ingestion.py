from src.exception import CustomException
from src.logger import logging

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def initiate_data_ingestion(self):
        try:
            logging.info("Started Data Ingestion.")
            df = pd.read_csv("data\ibm_hr.csv")
            logging.info(f"Dataset loaded with shape : {df.shape}")

            os.makedirs(os.path.dirname(self.data_ingestion_config.feature_store_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path),exist_ok=True)

            df.to_csv(self.data_ingestion_config.feature_store_file_path,index=False)
            logging.info("Feature store file saved.")

            train_data, test_data = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)

            train_data.to_csv(self.data_ingestion_config.training_file_path,index=False)
            test_data.to_csv(self.data_ingestion_config.testing_file_path,index=False)

            return DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
                feature_store_path=self.data_ingestion_config.feature_store_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        