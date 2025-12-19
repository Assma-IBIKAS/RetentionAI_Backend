from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

# Création du client Gemini
client = genai.Client(api_key=GENAI_API_KEY)


def generate_retention_plan(employee, churn_probability: float) -> list:
    """
    Génère un plan de rétention RH personnalisé
    à partir des données employé et de la probabilité de churn
    """

    # Sécurité : convertir en dict si Pydantic
    if hasattr(employee, "dict"):
        employee = employee.dict()

    # Règle métier : pas de plan si risque faible
    if churn_probability < 0.5:
        return []

    try:
        prompt = f"""
Tu es un expert senior en Ressources Humaines et en rétention des talents.

Voici les informations sur l’employé :

- Âge : {employee.get("Age")}
- Département : {employee.get("Department")}
- Poste : {employee.get("JobRole")}
- Niveau hiérarchique : {employee.get("JobLevel")}
- Satisfaction au travail : {employee.get("JobSatisfaction")}/4
- Implication : {employee.get("JobInvolvement")}/4
- Performance : {employee.get("PerformanceRating")}/4
- Équilibre vie professionnelle / personnelle : {employee.get("WorkLifeBalance")}/4
- Heures supplémentaires : {employee.get("OverTime")}

Contexte :
Le modèle de Machine Learning a estimé une probabilité de départ volontaire
de {round(churn_probability * 100, 2)}%.

Tâche :
Propose exactement 3 actions concrètes, réalistes et personnalisées
pour réduire le risque de départ de cet employé.

Contraintes :
- Actions applicables par un manager RH
- Adaptées au poste et au niveau de satisfaction
- Liste claire et opérationnelle
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=1)
            )
        )

        actions = [
            a.strip("- ").strip()
            for a in response.text.split("\n")
            if a.strip()
        ]

        return actions[:3]

    except Exception as e:
        print("Erreur Gemini :", e)
        return []
