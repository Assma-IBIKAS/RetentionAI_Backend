import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

# fonction pour charger les données 
def load_data(data):
    data = pd.read_csv(data)
    return data

# fonction pour visualiser les données catégorielles avec countplot
def count_plot(data, column,hue='Attrition'):
    plt.figure(figsize=(8,4))
    sns.countplot(x=column, data=data, hue=hue,palette="pastel")
    plt.title(f"Count Plot de {column}" + (f" par {hue}" if hue else ""))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# fonction pour visualiser les données numériques avec matrice de correlation 
def correlation(df):
    df = df.copy()
    df['Attrition'] = df['Attrition'].map({'No': 0, 'Yes': 1})
    corr = df.corr()
    plt.figure(figsize=(20,10))
    sns.heatmap(corr,annot=True,cmap="Purples",fmt=".2f")
    plt.show()

# #preparer le data, diviser notre ensemble de données en features and target 
# def prepare_data(data, target, colonnes_a_droper=[]):
#     X = data.drop(colonnes_a_droper,axis=1)
#     y = data[target]
#     return X, y

def prepare_data(data):
    # dropper les colonnes inutiles 
    columns_to_drop = [
        'Attrition',
        'EmployeeCount',
        'EmployeeNumber',
        'StandardHours',
        'Over18',
        'YearsSinceLastPromotion',
        'TrainingTimesLastYear',
        'PercentSalaryHike',
        'NumCompaniesWorked',
        'MonthlyRate',
        'HourlyRate',
        'DistanceFromHome',
        'DailyRate'
    ]
    # Séparer X et y
    X = data.drop(columns_to_drop, errors='ignore')
    y = data['Attrition']

    #garder les colonnes numériques en supprimons les colonnes déja encodés
    num_features = X.select_dtypes(exclude='object').columns.drop(
        ['Education','EnvironmentSatisfaction','JobInvolvement',
        'JobSatisfaction','PerformanceRating','RelationshipSatisfaction','WorkLifeBalance'], 
        errors='ignore'
    )
    #garder les colonnes catégorielles
    cat_features = X.select_dtypes(include='object').columns

    # Colonnes déjà encodées 
    colonne_cat_encod = ['Education','EnvironmentSatisfaction','JobInvolvement',
            'JobSatisfaction','PerformanceRating','RelationshipSatisfaction','WorkLifeBalance']

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, cat_features, num_features, colonne_cat_encod


def train_model_with_grid(X_train, y_train, X_num, X_cat, X_cat_encoded, model_type='rf'):
    """
    Entraîne un modèle de classification (RF ou Logistic Regression) avec pipeline complet et GridSearchCV
    """
    # Prétraitement
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), X_num),
            ('cat_txt', OneHotEncoder(handle_unknown='ignore'), X_cat),
            ('cat_encod', 'passthrough', X_cat_encoded)
        ]
    )

    # Choix du modèle et grille de paramètres
    if model_type == 'rf':
        model = RandomForestClassifier(random_state=42)
        param_grid = {
            'feature_selection__k': [5, 8, 10],
            'classifier__n_estimators': [100, 200],
            'classifier__max_depth': [None, 5, 10],
            'classifier__min_samples_split': [2, 5],
            'classifier__min_samples_leaf': [1, 2]
        }
    elif model_type == 'lr':
        model = LogisticRegression(max_iter=1000, random_state=42)
        param_grid = {
            'feature_selection__k': [5, 8, 10],
            'classifier__C': [0.1, 1, 10],
            'classifier__solver': ['lbfgs', 'liblinear']
        }
    else:
        raise ValueError("model_type doit être 'rf' ou 'logreg'")

    # Pipeline complet
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('feature_selection', SelectKBest(score_func=f_classif)),
        ('classifier', model)
    ])

    # GridSearchCV
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=5,
        scoring='roc_auc',  # On optimise le ROC-AUC pour classification
        n_jobs=-1
    )

    # Entraînement
    grid_search.fit(X_train, y_train)

    return grid_search