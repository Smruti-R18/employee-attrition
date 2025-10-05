from datetime import datetime
import os
from src.constants import constants

class TrainingPipelineConfig:
    def __init__(self):
        self.pipeline_name = constants.PIPELINE_NAME
        self.artifact_name = constants.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,constants.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,constants.DATA_INGESTION_FEATURE_STORE,constants.FILE_NAME)
        self.training_file_path = os.path.join(self.data_ingestion_dir,constants.DATA_INGESTION_INGESTED_DIR,constants.TRAIN_FILE_NAME)
        self.testing_file_path = os.path.join(self.data_ingestion_dir,constants.DATA_INGESTION_INGESTED_DIR,constants.TEST_FILE_NAME)
        self.train_test_split_ratio = constants.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,constants.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_data_dir = os.path.join(self.data_transformation_dir,constants.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR)
        self.transformed_object_dir  = os.path.join(self.data_transformation_dir,constants.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)

        self.transformed_training_file_path = os.path.join(self.transformed_data_dir,constants.TRANSFORMED_TRAIN_FILE_NAME)
        self.transformed_testing_file_path = os.path.join(self.transformed_data_dir,constants.TRANSFORMED_TEST_FILE_NAME)
        self.preprocessor_object_file_path = os.path.join(self.transformed_object_dir,constants.PREPROCESSOR_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.trained_model_file_path = os.path.join(constants.ARTIFACT_DIR,constants.MODEL_TRAINER_DIR,constants.TRAINED_MODEL_FILE_NAME)
        