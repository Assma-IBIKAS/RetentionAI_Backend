from backend.database.db import engine, Base
from backend.models.user_model import users
from backend.models.prediction_model import PredictionsHistory

from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from backend.database.db import getdb
from backend.models.user_model import users
from backend.schemas.user_schema import user_schema
from backend.services.security import hash_password
from backend.services.security import verify_password, create_access_token

from backend.schemas.employee_schema import employee_schema
from backend.services.ml_service import predict_churn
from backend.services.dependencies import get_current_user
from backend.services.gemini_service import generate_retention_plan

app = FastAPI(title="RetentionAI Backend")

# Création des tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "RetentionAI backend running"}

# @app.post("/register")
# def register(user: user_schema, db: Session = Depends(getdb)):
#     new_user = users(
#         username=user.username,
#         passwordhash=hash_password(user.password)
#     )
#     db.add(new_user)
#     db.commit()
#     return {"message": "User created successfully"}

# @app.post("/login")
# def login(user: user_schema, db: Session = Depends(getdb)):
#     db_user = db.query(users).filter(users.username == user.username).first()
#     if not db_user or not verify_password(user.password, db_user.passwordhash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": db_user.username, "user_id": db_user.id})
#     return {"access_token": token, "token_type": "bearer"}

# @app.post("/predict")
# def predict(
#     employee: employee_schema,
#     current_user = Depends(get_current_user),
#     db: Session = Depends(getdb)
# ):
#     proba = predict_churn(employee.dict())

#     history = PredictionsHistory(
#         user_id=current_user["user_id"],
#         employee_id=1,
#         probability=proba
#     )
#     db.add(history)
#     db.commit()

#     return {"churn_probability": proba}

# @app.post("/generate-retention-plan")
# def generate_plan(
#     employee: employee_schema,
#     churn_probability: float,
#     user=Depends(get_current_user)
# ):
#     plan = generate_retention_plan(employee, churn_probability)
#     return {"retention_plan": plan}
