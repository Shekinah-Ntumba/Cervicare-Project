import joblib
import pandas as pd
import os

# Load the trained model
MODEL_PATH = os.path.join("model", "cancer_predictor.pkl")
model = joblib.load(MODEL_PATH)

# (Optional) Add preprocessing steps if your model requires it

def run_batch_prediction(file_path: str):
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Ensure expected input features
        required_columns = ['age', 'smoking', 'hpv_result']  # Update this list based on your model
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Input file missing required columns.")

        input_data = df[required_columns]
        predictions = model.predict(input_data)

        df["prediction"] = predictions
        return df.to_dict(orient="records")

    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
