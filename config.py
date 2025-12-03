# Configuration du projet
import os

# Chemins des répertoires
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
CLEANED_DATA_DIR = os.path.join(DATA_DIR, 'cleaned')
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Fichiers de données
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, 'rawdata.csv')
CLEANED_DATA_FILE = os.path.join(CLEANED_DATA_DIR, 'cleaneddata.csv')

# Configuration du dashboard
DEBUG = True
PORT = 8050
HOST = '127.0.0.1'
