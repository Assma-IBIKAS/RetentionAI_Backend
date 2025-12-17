import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

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
    df['Attrition'] = df['Attrition'].map({'No': 0, 'Yes': 1})
    corr = df.corr()
    plt.figure(figsize=(20,10))
    sns.heatmap(corr,annot=True,cmap="Purples",fmt=".2f")
    plt.show()