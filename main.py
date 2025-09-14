import os
import sys
from src.exception import CustomException
from src.logger import logging

from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataTransformationConfig, ModelTrainerConfig
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


def main():
    try:
        logging.info("Pipeline started.")
        training_pipeline_config = TrainingPipelineConfig()

        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed.")
        print(data_ingestion_artifact)

        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,data_transformation_config=data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed.")
        print(data_transformation_artifact)

        model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_config=model_trainer_config
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training completed.")
        print(model_trainer_artifact)

        print("\n======= Final Results =======")
        print(f"Best Model: {model_trainer_artifact.best_model_name}")
        print(f"Best Model F1 Score: {model_trainer_artifact.best_model_score:.4f}")
        print(f"Saved Model Path: {model_trainer_artifact.trained_model_file_path}")
        print("=============================\n")

        logging.info("Pipeline execution completed")

    except Exception as e:
        raise(CustomException(e,sys))
    
if __name__ == "__main__":
    main()
