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