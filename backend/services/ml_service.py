import joblib

model = joblib.load("ML/lr_model.pkl")
pipeline = joblib.load("ML/pipeline.pkl")

def predict_churn(data):
    X = pipeline.transform([data])
    proba = model.predict_proba(X)[0][1]
    return float(proba)
