import joblib

# Charger le modèle
model = joblib.load("ML/lr_model.pkl")


def predict_churn(data):
    """
    data : liste ou array des features déjà préparées
    """
    # Si model est un pipeline, il gère la transformation automatiquement
    # Si model est juste le modèle, data doit être déjà transformé
    proba = model.predict_proba([data])[0][1]
    return float(proba)