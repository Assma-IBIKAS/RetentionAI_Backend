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
    Génère un plan de rétention RH personnalisé à partir
    des données employé et de la probabilité de churn
    """

    # Règle métier : pas de plan si risque faible
    if churn_probability < 0.5:
        return []

    try:
        # Prompt Engineering RH
        prompt = f"""
Tu es un expert senior en Ressources Humaines et en rétention des talents.

Voici les informations sur l’employé :

- Âge : {employee.Age}
- Département : {employee.Department}
- Poste : {employee.JobRole}
- Niveau hiérarchique : {employee.JobLevel}
- Satisfaction au travail : {employee.JobSatisfaction}/4
- Implication : {employee.JobInvolvement}/4
- Performance : {employee.PerformanceRating}/4
- Équilibre vie professionnelle / personnelle : {employee.WorkLifeBalance}/4
- Heures supplémentaires : {employee.OverTime}

Contexte :
Le modèle de Machine Learning a estimé une probabilité de départ volontaire
de {round(churn_probability * 100, 2)}%.

Tâche :
Propose exactement 3 actions concrètes, réalistes et personnalisées
pour réduire le risque de départ de cet employé.

Contraintes :
- Les actions doivent être applicables par un manager RH
- Elles doivent tenir compte du poste, de la satisfaction et de l’équilibre vie pro/perso
- Rédige les actions sous forme d’une liste claire et opérationnelle
"""

        # Appel Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=1)
            )
        )

        # Nettoyage de la réponse
        raw_text = response.text
        actions = raw_text.split("\n")
        actions = [a.strip("- ").strip() for a in actions if a.strip()]

        return actions[:3]

    except Exception as e:
        print("Erreur Gemini :", e)
        return []
