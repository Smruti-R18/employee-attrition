import os
import sys
from src.exception import CustomException
from src.logger import logging
import shutil

from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataTransformationConfig, ModelTrainerConfig
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


def main():
    try:
        logging.info("Training pipeline started.")

        # Step 1: Training pipeline config
        training_pipeline_config = TrainingPipelineConfig()

        # Step 2: Data ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed.")
        print(data_ingestion_artifact)

        # Step 3: Data transformation
        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_transformation_config=data_transformation_config
        )
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed.")
        print(data_transformation_artifact)

        # Step 4: Model training
        model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_config=model_trainer_config
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training completed.")
        print(model_trainer_artifact)

        # Copy final model and preprocessor to Artifacts folder
        os.makedirs("Artifacts", exist_ok=True)
        shutil.copy(model_trainer_artifact.trained_model_file_path, "Artifacts/model.pkl")
        shutil.copy(data_transformation_artifact.preprocessor_object_file_path, "Artifacts/preprocessor.pkl")

        print("\n======= Final Results =======")
        print(f"Best Model: {model_trainer_artifact.best_model_name}")
        print(f"Best Model F1 Score: {model_trainer_artifact.best_model_score:.4f}")
        print(f"Saved Model Path: Artifacts/model.pkl")
        print("=============================\n")

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
