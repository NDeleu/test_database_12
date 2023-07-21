from models import Administrator
from models import session


def check_administrator_existence():
    # Compte le nombre d'administrateurs dans la table 'administrators'
    num_administrators = session.query(Administrator).count()

    return num_administrators > 0
