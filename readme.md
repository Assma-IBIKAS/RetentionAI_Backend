# 🚀 RetentionAI : Plateforme Prédictive de Rétention RH 
RetentionAI est une solution full-stack innovante qui permet aux directions des Ressources Humaines de passer d'une gestion réactive à une gestion proactive du turnover. En combinant le Machine Learning supervisé et l'IA Générative, l'application prédit les risques de départs et propose des plans d'action immédiats.

# 📋 Table des Matières ##
+ Contexte & Objectifs

+ Architecture du Système

+ Stack Technique

+ Installation avec Docker

+ Documentation de l'API

+ Structure du Projet

# 🎯 Contexte & Objectifs
## Problématique
Les départs volontaires coûtent cher et désorganisent les équipes. Actuellement, les RH analysent les départs une fois qu'ils ont eu lieu.

## Mission de RetentionAI
1. Anticiper : Identifier les profils à haut risque via un score de probabilité.

1. Agir : Générer 3 recommandations personnalisées par employé via un LLM (Gemini/HuggingFace).

1. Sécuriser : Garantir la confidentialité des données RH via une authentification JWT et une traçabilité complète.

Voici le contenu complet de votre fichier README.md. Vous pouvez copier ce bloc de texte et l'enregistrer dans un fichier nommé README.md à la racine de votre projet.

🚀 RetentionAI : Plateforme Prédictive de Rétention RH
RetentionAI est une solution full-stack innovante qui permet aux directions des Ressources Humaines de passer d'une gestion réactive à une gestion proactive du turnover. En combinant le Machine Learning supervisé et l'IA Générative, l'application prédit les risques de départs et propose des plans d'action immédiats.

📋 Table des Matières
Contexte & Objectifs

Architecture du Système

Stack Technique

Installation avec Docker

Documentation de l'API

Structure du Projet

🎯 Contexte & Objectifs
Problématique
Les départs volontaires coûtent cher et désorganisent les équipes. Actuellement, les RH analysent les départs une fois qu'ils ont eu lieu.

Mission de RetentionAI
Anticiper : Identifier les profils à haut risque via un score de probabilité.

Agir : Générer 3 recommandations personnalisées par employé via un LLM (Gemini/HuggingFace).

Sécuriser : Garantir la confidentialité des données RH via une authentification JWT et une traçabilité complète.

# 🏗 Architecture du Système
Le flux de données suit ce parcours :

1. L'utilisateur RH saisit les données de l'employé sur le Frontend (Next.js).

1. Le Backend (FastAPI) authentifie la requête et interroge le modèle.

1. Si le risque est > 50%, le système sollicite l'IA Générative pour créer un plan de rétention.

1. L'historique est sauvegardé dans PostgreSQL pour audit.
# 🛠 Stack Technique
| Composant           | Technologie                                   |
|--------------------|-----------------------------------------------|
| Frontend           | Next.js (React), Tailwind CSS                 |
| Backend            | FastAPI (Python), SQLAlchemy                  |
| Base de Données    | PostgreSQL                                    |
| Machine Learning   | Scikit-learn, Pandas, Seaborn, Matplotlib         |
| IA Générative      | Google Gemini API Face              |
| DevOps             | Docker, Docker Compose, Pytest                |

# 🛣 Documentation de l'API
## Authentification
- ````POST /register```` :: Création de compte RH (Mot de passe haché avec Bcrypt).
- ``POST /login``: Génération du token JWT.
## Prédiction & Intelligence
- ````POST /predict```` : Reçoit les features de l'employé et retourne la ``churn_probability``.
- ``POST /generate-retention-plan``: Génère un plan de rétention si le risque est avéré.