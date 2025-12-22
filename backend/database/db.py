from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv
import os

# Charger le fichier .env
# dotenv_path = BASE_DIR / ".env"
# load_dotenv(dotenv_path=dotenv_path)
load_dotenv()

# Récupérer les variables d'environnement
USER_DB = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

# Créer l'URL de connexion
# DATABASE_URL = f"postgresql://{USER_DB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:0000@localhost:5432/retention")
DATABASE_URL = os.getenv("DATABASE_URL")

# Créer l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Créer la session locale
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Déclarative Base
Base = declarative_base()

# Fonction pour obtenir une session
def getdb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


