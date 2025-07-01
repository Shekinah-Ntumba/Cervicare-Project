import joblib
import pandas as pd
import os

# Load the trained model
MODEL_PATH = os.path.join("model", "cancer_predictor.pkl")
model = joblib.load(MODEL_PATH)

# def run_batch_prediction(file_path: str):
#     try:
#         if file_path.endswith(".csv"):
#             df = pd.read_csv(file_path)
#         else:
#             df = pd.read_excel(file_path)

#         required_columns = ['age', 'blood_pressure', 'hpv_result', 'screening_history', 'smoking_status']
#         if not all(col in df.columns for col in required_columns):
#             raise ValueError("Input file missing required columns.")

#         input_data = df[required_columns]
#         predictions = model.predict(input_data)

#         df["prediction"] = predictions
#         return df.to_dict(orient="records")

#     except Exception as e:
#         raise RuntimeError(f"Prediction failed: {str(e)}")
def run_batch_prediction(file_path: str):
    try:
        print("📂 Reading file:", file_path)

        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        print("🧾 Columns in uploaded file:", df.columns.tolist())

        required_columns = ['age', 'blood_pressure', 'hpv_result', 'screening_history', 'smoking_status']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing columns. Required: {required_columns}")

        input_data = df[required_columns]
        print("📊 Input data preview:\n", input_data.head())
        print("📏 Input shape:", input_data.shape)

        predictions = model.predict(input_data)
        print("✅ Predictions:", predictions)

        df["prediction"] = predictions
        return df.to_dict(orient="records")

    except Exception as e:
        print("❌ Prediction failed:", str(e))  # Log actual error
        raise RuntimeError(f"Prediction failed: {str(e)}")
