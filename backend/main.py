from backend.database.db import engine, Base 
from backend.models.user_model import users
from backend.models.prediction_model import PredictionsHistory
from backend.schemas.user_schema import *
from fastapi import FastAPI,Depends,HTTPException, status
from sqlalchemy.orm import Session
from backend.database.db import getdb
from backend.models.user_model import users
# from backend.schemas.user_schema import user_schema
from backend.services.security import hash_password
from backend.services.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

from backend.schemas.employee_schema import employee_schema, GeneratePlanRequest
from backend.services.ml_service import predict_churn
from backend.services.dependencies import get_current_user
from backend.services.gemini_service import generate_retention_plan
import pandas as pd

app = FastAPI(title="RetentionAI Backend")

# Création des tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "RetentionAI backend running"}

# Endpoint de Register
@app.post("/Register")
def signup(user: user_schema,db: Session = Depends(getdb)):
    # Hasher le password
    hashed_pw = hash_password(user.password)

    # Remplacer password par password_hash
    db_user = users(
        username=user.username,
        password_hash=hashed_pw
    )

    # Enregistrer l’utilisateur
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User Created !!"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getdb)):
    # Chercher l'utilisateur
    db_user = db.query(users).filter(users.username == form_data.username).first()

    # Vérifier l'existence et le mot de passe
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Créer le token JWT
    token = create_access_token({"sub": db_user.username, "user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}


import pandas as pd

@app.post("/predict")
def predict(
    employee: employee_schema,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(getdb)
):
    # DataFrame 1 ligne
    data = pd.DataFrame([employee.dict()])

    # Prédiction
    proba = predict_churn(data)

    # Sauvegarde
    history = PredictionsHistory(
        user_id=current_user["user_id"],
        probability=proba
    )
    db.add(history)
    db.commit()
    db.refresh(history)

    return {
        "prediction_id": history.id,
        "user_id": current_user["user_id"],
        "churn_probability": proba
    }



@app.post("/generate-retention-plan")
def generate_plan(
    payload: GeneratePlanRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(getdb)
):
    # Récupérer la prédiction
    prediction = db.query(PredictionsHistory).filter(
        PredictionsHistory.id == payload.prediction_id,
        PredictionsHistory.user_id == current_user["user_id"]
    ).first()

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    # Générer le plan
    plan = generate_retention_plan(
        churn_probability=prediction.probability
    )

    return {
        "prediction_id": prediction.id,
        "user_id": current_user["user_id"],
        "retention_plan": plan
    }

