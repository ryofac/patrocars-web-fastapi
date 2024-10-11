from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from patrocars.settings import settings

engine = create_engine(settings.DB_URL)


def get_db():
    with Session(engine) as session:
        try:
            yield session
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
