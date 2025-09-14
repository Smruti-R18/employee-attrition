import os
import sys
import joblib

from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score


def save_object(file_path, obj):
    try:
        logging.info("Entered save_object method of utils.py")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            joblib.dump(obj, file_obj)
        logging.info("Exited save_object of utils.py")
    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        logging.info(f"Loading object from {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        with open(file_path, "rb") as file_obj:
            return joblib.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        best_model = None
        best_score = 0
        best_model_name = None

        for model_name, model in models.items():
            param_grid = params.get(model_name, None)

            if param_grid and len(param_grid) > 0:
                gs = GridSearchCV(model, param_grid, cv=3, scoring="f1_weighted", n_jobs=-1)
                gs.fit(X_train, y_train)
                best_estimator = gs.best_estimator_
            else:
                best_estimator = model
                best_estimator.fit(X_train, y_train)

            y_test_pred = best_estimator.predict(X_test)
            test_f1 = f1_score(y_test, y_test_pred, average="weighted")

            report[model_name] = test_f1

            if test_f1 > best_score:
                best_score = test_f1
                best_model = best_estimator
                best_model_name = model_name

        return report, best_model_name, best_model, best_score

    except Exception as e:
        raise CustomException(e, sys)
