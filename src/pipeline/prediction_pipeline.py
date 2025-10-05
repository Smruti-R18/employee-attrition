import os
import sys
import pandas as pd
from src.utils import load_object
from src.exception import CustomException
from src.logger import logging


class PredictionPipeline:
    def __init__(self, model_path: str, preprocessor_path: str):
        try:
            logging.info("Loading model and preprocessor in PredictionPipeline")
            self.model = load_object(model_path)

            # Load preprocessor (only needed if model doesn't include one)
            try:
                self.preprocessor = load_object(preprocessor_path)
            except Exception as e:
                logging.warning(f"Could not load standalone preprocessor: {e}")
                self.preprocessor = None

        except Exception as e:
            raise CustomException(e, sys)

    def predict_from_file(self, file_path):
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Loaded input file with shape {df.shape}")

            # Detect if model already includes a preprocessor
            has_preprocessor = False
            if hasattr(self.model, "named_steps"):
                has_preprocessor = "preprocessor" in self.model.named_steps

            # Prepare data accordingly
            if has_preprocessor:
                logging.info("Model already includes preprocessor — using raw data.")
                probabilities = self.model.predict_proba(df)[:, 1]
            elif self.preprocessor is not None:
                logging.info("Using external preprocessor before prediction.")
                X_transformed = self.preprocessor.transform(df)
                probabilities = self.model.predict_proba(X_transformed)[:, 1]
            else:
                raise CustomException("No preprocessor found in model or separately.", sys)

            # Add predictions
            df['Attrition_Probability'] = probabilities

            def risk_category(p):
                if p >= 0.6:
                    return 'High-risk'
                elif 0.5 <= p < 0.6:
                    return 'Medium-risk'
                else:
                    return 'Low-risk'
                
            df['Attrition_Prediction'] = [risk_category(p) for p in probabilities]
            #df['Attrition_Prediction'] = ['Yes' if p >= 0.6 else 'No' for p in probabilities]

            # Save result
            os.makedirs("uploads", exist_ok=True)
            output_path = os.path.join("uploads", "predictions.csv")
            df.to_csv(output_path, index=False)

            logging.info(f"Predictions saved to {output_path}")
            return output_path

        except Exception as e:
            raise CustomException(e, sys)
