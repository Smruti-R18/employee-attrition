import os
import sys
from src.exception import CustomException
from src.logger import logging

from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from src.components.data_ingestion import DataIngestion

def main():
    try:
        logging.info("Pipeline started.")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        train_path, test_path = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed.")
        logging.info(f"Train file path : {train_path}")
        logging.info(f"Test file path : {test_path}")

    except Exception as e:
        raise(CustomException(e,sys))
    
if __name__ == "__main__":
    main()
