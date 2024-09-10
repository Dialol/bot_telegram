from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()
DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    birthdate = Column(String, nullable=False)


def save_client_data_to_db(user_id, name, city, birthdate):
    db_session = SessionLocal()
    new_client = Client(
        user_id=user_id,
        name=name,
        city=city,
        birthdate=birthdate
    )
    db_session.add(new_client)
    db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
