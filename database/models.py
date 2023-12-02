from sqlalchemy.orm import declarative_base, sessionmaker, relationship, \
    validates
from sqlalchemy import (create_engine, Column, String, Integer, Boolean,
                        DateTime, ForeignKey)

from utils.security import generate_password_hash, check_password_hash
from utils.validators import validate_email, validate_telephone_number

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

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @validates("email")
    def validate_email(self, key, email):
        return validate_email(email) and email

    @validates("telephone_number")
    def validate_telephone_number(self, key, telephone_number):
        return (validate_telephone_number(telephone_number)
                and telephone_number)

    def __repr__(self):
        return (f"<User: {self.email} -- {self.telephone_number}, "
                f"{self.created_at}>")

    def __str__(self):
        return f"{self.firstname}, {self.telephone_number}"


class Child(Base):
    __tablename__ = "children"

    child_id = Column(Integer, primary_key=True, unique=True,
                      nullable=False, autoincrement=True)
    parent_id = Column(String, ForeignKey("users.email"), nullable=False)
    name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=False, index=True)
    
    def __str__(self):
        return f"{self.name}, {self.age}"

    def __repr__(self):
        return f"<Child: {self.__str__()}>"
