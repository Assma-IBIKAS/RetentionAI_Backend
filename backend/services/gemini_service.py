from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

# Création du client Gemini
client = genai.Client(api_key=GENAI_API_KEY)


def generate_retention_plan(churn_probability: float) -> list:
    """
    Génère un plan de rétention RH personnalisé
    uniquement basé sur la probabilité de churn.
    """

    # Règle métier : pas de plan si risque faible
    if churn_probability < 0.5:
        return []

    try:
        # Prompt simple basé uniquement sur la probabilité
        prompt = f"""
Tu es un expert senior en Ressources Humaines.

Le modèle de Machine Learning a estimé une probabilité
de départ volontaire de {round(churn_probability * 100, 2)}%.

Tâche :
Propose exactement 3 actions concrètes, réalistes
et adaptées pour réduire le risque de départ.

Contraintes :
- Actions applicables par un manager RH
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

