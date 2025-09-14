import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from imblearn.over_sampling import SMOTE

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact
from src.constants import constants
from src.utils import save_object

from src.exception import CustomException
from src.logger import logging

class DataTransformation():
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_transformation_config:DataTransformationConfig):
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifact = data_ingestion_artifact

    def fetch_numerical_features(self,df):
        numerical_features = [col for col in df.columns if df[col].dtype!='O']
        return numerical_features
    
    def fetch_categorical_features(self,df):
        categorical_features = [col for col in df.columns if df[col].dtype=='O']
        return categorical_features
    
    def initiate_data_transformation(self):
        try:
            logging.info("Data Transformation started.")
            train_data = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_data = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            drop_col = ['EmployeeCount','EmployeeNumber','Over18','StandardHours']
            train_data.drop(columns=drop_col,axis=1,inplace=True,errors='ignore')
            test_data.drop(columns=drop_col,axis=1,inplace=True,errors='ignore')
            logging.info(f"Dropped columns : {drop_col}")

            X_train = train_data.drop(columns=['Attrition'])
            y_train = train_data[constants.TARGET_COLUMN]
            X_test = test_data.drop(columns=['Attrition'])
            y_test = test_data[constants.TARGET_COLUMN]
            logging.info("Split the dependent and independent features")

            y_train = y_train.replace({'Yes':0, 'No':1})
            y_test = y_test.replace({'Yes':0, 'No':1})

            numerical_features = self.fetch_numerical_features(X_train)
            categorical_features = self.fetch_categorical_features(X_train)

            num_pipeline = Pipeline([
                ('scaler',StandardScaler())
            ])

            cat_pipeline = Pipeline([
                ('encoder',OneHotEncoder(handle_unknown='ignore'))
            ])

            preprocessor = ColumnTransformer([
                ('num',num_pipeline,numerical_features),
                ('cat',cat_pipeline,categorical_features)
            ])

            X_train.columns = X_train.columns.astype(str)
            X_test.columns = X_test.columns.astype(str)

            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)

            logging.info(f"Before SMOTE: {y_train.value_counts().to_dict()}")
            smote = SMOTE(random_state=42)
            X_train_transformed, y_train = smote.fit_resample(X_train_transformed, y_train)
            logging.info(f"After SMOTE: {pd.Series(y_train).value_counts().to_dict()}")

            preprocessor_path = self.data_transformation_config.preprocessor_object_file_path
            save_object(preprocessor_path,preprocessor)

            logging.info("Created and saved preprocessor object.")

            transformed_train_path = self.data_transformation_config.transformed_training_file_path
            transformed_test_path = self.data_transformation_config.transformed_testing_file_path

            os.makedirs(os.path.dirname(transformed_train_path), exist_ok=True)
            os.makedirs(os.path.dirname(transformed_test_path), exist_ok=True)

            np.savez(transformed_train_path, X=X_train_transformed, y=y_train.to_numpy())
            np.savez(transformed_test_path, X=X_test_transformed, y=y_test.to_numpy())
            logging.info("Saved transformed train and test data as .npz files")

            # Create artifact
            data_transformation_artifact = DataTransformationArtifact(
                preprocessor_object_file_path=preprocessor_path,
                transformed_train_file_path=transformed_train_path,
                transformed_test_file_path=transformed_test_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)
    