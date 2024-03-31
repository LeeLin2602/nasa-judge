from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

from models import db

class Profile:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_profile(self):
        session = self.session_factory()
        try:
            profile = db.WireguardProfile(
                valid=True,
            )
            session.add(profile)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def del_profile(self, profile_id):
        session = self.session_factory()
        try:
            profile = session.query(db.WireguardProfile).filter_by(profile_id=profile_id).first()
            if profile:
                profile.valid = False
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
