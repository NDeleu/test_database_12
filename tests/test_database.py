import pytest
import os
from configparser import ConfigParser
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database

# Importez vos modèles de classes existants
from models.class_models.administrator import Administrator
from models.class_models.client import Client
from models.class_models.article import Article


@pytest.fixture(scope='session')
def postgresql():
    """Fixture for PostgreSQL database."""
    # Détails de connexion

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    config_file = os.path.join(root_dir, 'config.ini')

    config = ConfigParser()
    config.read(config_file)

    username = config.get('sql', 'username')
    password = config.get('sql', 'password')
    database_name = config.get('sql', 'database_name')

    info = {
        'user': f'{username}',
        'password': f'{password}',
        'host': 'localhost',
        'port': 5432,
        'dbname': f'{database_name}',
    }

    yield info


@pytest.fixture
def db_session(postgresql):
    """Session for SQLAlchemy."""
    from models import Base

    # Créez la base de données temporaire en ajoutant "_test" au nom de la base de données existante
    test_db_name = f"{postgresql['dbname']}_test"

    db_url = f"postgresql://{postgresql['user']}:{postgresql['password']}@{postgresql['host']}:{postgresql['port']}/{test_db_name}"

    # Vérifiez si la base de données existe et créez-la si nécessaire
    if not database_exists(db_url):
        create_database(db_url)

    # Créez un moteur SQLAlchemy et une session
    engine = create_engine(db_url, echo=False, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Copiez les tables existantes vers la base de données temporaire
    Base.metadata.create_all(engine)

    # Si vous utilisez Alembic pour la gestion des migrations, vous pouvez exécuter les migrations ici

    yield session

    session.close()
    engine.dispose()

    # Supprimez la base de données temporaire une fois les tests terminés
    if database_exists(db_url):
        drop_database(db_url)


def test_database_connection(db_session):
    # Vérifiez si la connexion à la base de données fonctionne

    # Exemple de requête pour vérifier si la connexion est réussie
    result = db_session.execute(text("SELECT 1"))

    # Vérifiez si la requête a renvoyé le résultat attendu
    assert result.scalar() == 1

    # Vous pouvez également effectuer d'autres vérifications, par exemple,
    # vérifier si une table spécifique existe ou si vous pouvez insérer et récupérer des données.

    # Exemple de vérification si une table spécifique existe
    table_exists = db_session.connection().execute(text("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='administrators')")).scalar()

    # Vérifiez si la table existe
    assert table_exists

    # Vous pouvez ajouter d'autres vérifications spécifiques à votre cas d'utilisation


def test_create_administrator(db_session):
    # Créez un nouvel administrateur
    administrator = Administrator.create(surname="Jean", lastname="Delafontaine", age=30, email="PoeteAvantTout@example.com", password="jeanpass")

    # Vérifiez si l'administrateur a été créé avec succès en le récupérant de la base de données
    created_administrator = Administrator.read(administrator.id)
    assert created_administrator is not None

    # Vérifiez les valeurs des attributs de l'administrateur créé
    assert created_administrator.surname == "Jean"
    assert created_administrator.lastname == "Delafontaine"
    assert created_administrator.age == 30
    assert created_administrator.email == "PoeteAvantTout@example.com"
    assert created_administrator.verify_password("jeanpass")

    # Supprimez l'administrateur pour nettoyer la base de données
    created_administrator.delete()
