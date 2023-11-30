from sqlalchemy.orm import declarative_base, sessionmaker, relationship, \
    validates
from sqlalchemy import (create_engine, Column, String, Integer, Boolean,
                        DateTime, ForeignKey)

from utils.email_validator import validate_email

Base = declarative_base()


def start_engine(engine_url="sqlite:///:memory:"):
    engine = create_engine(engine_url)
    Session = sessionmaker(engine)
    session = Session()
    Base.metadata.create_all(engine)

    return engine, session


def drop_all(engine):
    Base.metadata.drop_all(engine)


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, unique=True,
                     nullable=False, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    default = Column(Boolean, default=False)
    users = relationship("User", backref="role", lazy="dynamic")


class User(Base):
    __tablename__ = "users"

    email = Column(String(320), unique=True, primary_key=True,
                   nullable=False)
    firstname = Column(String(128), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    telephone_number = Column(String(9), unique=True, index=True,
                              nullable=False)
    children = relationship("Child", backref="parent",
                            lazy="dynamic", cascade="all, delete-orphan")
    # hash will be generated using hashlib.sha256().hexdigest
    password_hash = Column(String(64))
    created_at = Column(DateTime, nullable=False)

    @validates("email")
    def validate_email(self, key, email):
        return validate_email(email) and email


class Child(Base):
    __tablename__ = "children"

    child_id = Column(Integer, primary_key=True, unique=True,
                      nullable=False, autoincrement=True)
    parent_id = Column(String, ForeignKey("users.email"), nullable=False)
    name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=False, index=True)
