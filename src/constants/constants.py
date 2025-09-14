import os
import sys
import numpy as np
import pandas as pd

"""
Common Constants
"""
TARGET_COLUMN = "Attrition"
PIPELINE_NAME = "EmployeeAttrition"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "ibm_hr.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

"""
Data Ingestion Constants
"""
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2

"""
Data Transformation Constants
"""
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"

PREPROCESSOR_OBJECT_FILE_NAME = "preprocessor.pkl"
TRANSFORMED_TRAIN_FILE_NAME = "train.npz"
TRANSFORMED_TEST_FILE_NAME = "test.npz"

"""
Model Training Constants
"""
MODEL_TRAINER_DIR = "model_trainer"
TRAINED_MODEL_FILE_NAME = "model.pkl"