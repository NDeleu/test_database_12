from controllers import (cli,
                         first_init_bdd,
                         check_administrator_existence,
                         create_first_administrator)
from sqlalchemy.exc import SQLAlchemyError


if __name__ == '__main__':
    try:
        if check_administrator_existence():
            cli()
        else:
            create_first_administrator()
    except SQLAlchemyError:
        first_init_bdd()
