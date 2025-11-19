# src/pipeline/prediction_pipeline.py
import os
import sys
import pandas as pd
import numpy as np

from src.utils import load_object
from src.recommendations import generate_recommendation
from src.exception import CustomException
from src.logger import logging

class PredictionPipeline:
    def __init__(self, model_path, preprocessor_path):
        self.model = load_object(model_path)

        try:
            self.preprocessor = load_object(preprocessor_path)
        except:
            self.preprocessor = None

    def predict_from_file(self, file_path):
        try:
            df = pd.read_csv(file_path)
            raw_df = df.copy()

            has_pre = hasattr(self.model, "named_steps") and "preprocessor" in self.model.named_steps

            if has_pre:
                X = df
            else:
                X = self.preprocessor.transform(df)

            if hasattr(self.model, "predict_proba"):
                prob = self.model.predict_proba(X)[:, 1]
            else:
                pred = self.model.predict(X)
                prob = np.array([float(p) for p in pred])

            df["Attrition_Probability"] = prob
            df["Attrition_Prediction"] = ["High-risk" if p >= 0.75 else ("Medium-risk" if p >= 0.40 else "Low-risk") for p in prob]

            # ------------------------
            # Recommendations + ID
            # ------------------------
            recs_list = []
            ids_list = []
            for idx, row in raw_df.iterrows():
                row_dict = row.to_dict()
                display_id, risk, recs = generate_recommendation(row_dict, float(prob[idx]))
                ids_list.append(display_id)
                recs_list.append(','.join(recs))

            df["Employee_ID"] = ids_list
            df["Recommendations"] = recs_list

            out = os.path.join("uploads", "predictions.csv")
            df.to_csv(out, index=False)
            return out

        except Exception as e:
            raise CustomException(e, sys)
