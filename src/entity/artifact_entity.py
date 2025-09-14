from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path : str
    test_file_path : str
    feature_store_path : str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path : str
    transformed_test_file_path : str
    preprocessor_object_file_path : str

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path : str
    best_model_name : str
    best_model_score : float