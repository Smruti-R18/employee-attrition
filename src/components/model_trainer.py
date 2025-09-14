import os
import sys
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline

from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,load_object,evaluate_models

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
    
    def initiate_model_trainer(self):
        try:
            logging.info("Entered initiate_model_training of model_trainer.py")

            train_data = np.load(self.data_transformation_artifact.transformed_train_file_path,allow_pickle=True)
            test_data = np.load(self.data_transformation_artifact.transformed_test_file_path,allow_pickle=True)

            X_train,y_train = train_data['X'],train_data['y']
            X_test,y_test = test_data['X'],test_data['y']

            logging.info(f"Train data shape : {X_train.shape}. Test data shape : {X_test.shape}")

            models = {
            "Logistic Regression" : LogisticRegression(max_iter=1500),
            "Random Forest" : RandomForestClassifier(verbose=1),
            "SVC" : SVC(probability=True),
            "KNN" : KNeighborsClassifier(),
            "Naive Bayes" : GaussianNB(),
            "AdaBoost" : AdaBoostClassifier(),
            "XGBBoost" : XGBClassifier(),
            "Gradient Boost" : GradientBoostingClassifier(verbose=1,random_state=42),
            "Decision Tree" : DecisionTreeClassifier(random_state=42)
            }

            param_grid = {
                "Logistic Regression" : {
                "C" : [0.01,0.1,1,10],
                "solver" :  ["lbfgs","liblinear","newton-cg","newton-cholesky","sag","saga"]
                },
                "Random Forest" : {
                    "criterion" : ["gini","entropy","log_loss"],
                    "max_features" : ["sqrt","log2",None],
                    "class_weight" : ["balanced","balanced_subsample"],
                    "n_estimators" : [100,200],
                    "max_depth" : [None,10,20]
                },
                "SVC" : {
                    "C" : [0.1,1,10],
                    "kernel" : ["linear","poly","rbf","sigmoid"],
                    "gamma" : ["scale","auto"],
                },
                "KNN" : {
                    "n_neighbors" : [3,5,7,11],
                    "weights" : ["uniform","distance"],
                    "algorithm" : ["auto","ball_tree","kd_tree","brute"],
                },
                "Naive Bayes" : {},
                "AdaBoost" : {
                    "n_estimators" : [50,100,200],
                    "learning_rate" : [0.01,0.1,1.0]
                },
                "XGBBoost" : {
                    "n_estimators" : [50,100,200],
                    "learning_rate" : [0.01,0.1,1.0],
                    "max_depth" : [3,5,7,9]
                },
                "Gradient Boost" : {
                    "n_estimators" : [50,100,200],
                    "learning_rate" : [0.01,0.1,1.0],
                    "max_depth" : [3,5,7,9]
                },
                "Decision Tree" : {
                    "max_depth" : [3,5,7,9],
                    "criterion" : ["gini","entropy","log_loss"],
                    "splitter" : ["best","random"]
                }
            }

            model_report,best_model_name,best_model,best_score = evaluate_models(X_train,y_train,X_test,y_test,models,param_grid)
            logging.info(f"Best Model : {best_model_name} with F1 score : {best_score : .4f}")

            preprocessor = load_object(self.data_transformation_artifact.preprocessor_object_file_path)
            logging.info("Preprocessor loaded successfully")

            final_pipeline = Pipeline([
                ("preprocessor",preprocessor),
                ("model",best_model)
            ])

            final_model_path = self.model_trainer_config.trained_model_file_path
            os.makedirs(os.path.dirname(final_model_path),exist_ok=True)
            save_object(final_model_path,final_pipeline)

            logging.info(f"Final model pipeline saved at {final_model_path}")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=final_model_path,
                best_model_name=best_model_name,
                best_model_score=best_score
            )

            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e,sys)