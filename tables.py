#Creación de la base de datos con sqlalchemy

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime

username = "danielmaster"
password = "CamelloMontante159"
host = "database-tek-d.czucmi2aq73b.us-east-2.rds.amazonaws.com"
database = "DataBase_TekD"

url = f"mysql+pymysql://{username}:{password}@{host}/{database}"
engine = create_engine(url)
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer(), primary_key=True)
    name = Column(String(60), nullable=False, unique=True)
    rfc = Column(String(13), nullable=False, unique=True)
    email = Column(String(60), nullable=False)
    street = Column(String(100), nullable=False)
    street_number = Column(String(10), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    cp = Column(String(10), nullable=False)
    city = Column(String(80), nullable=False)
    state = Column(String(80), nullable=False)
    country = Column(String(80), nullable=False)

    invoice = relationship("Invoice", back_populates="clients_table")

class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(Integer(), primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(200), nullable=False)
    product = Column(String(60), nullable=False)
    total = Column(Numeric(precision=10, scale=2), nullable=False)
    id_client = Column(Integer(), ForeignKey('clients.id'), nullable=False)

    clients_table = relationship("Client", back_populates="invoice")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer(), primary_key=True)
    name = Column(String(60), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    street = Column(String(100), nullable=False)
    street_number = Column(String(10), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    cp = Column(String(10), nullable=False)
    city = Column(String(80), nullable=False)
    state = Column(String(80), nullable=False)
    country = Column(String(80), nullable=False)
    area_id = Column(Integer(), ForeignKey('areas.id'), nullable=False)
    salary = Column(Numeric(precision=10, scale=2), nullable=False)
    hiring_date = Column(DateTime(), default=datetime.now, nullable=False)

    area_table = relationship("Area", back_populates="employees")

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer(), primary_key=True)
    name = Column(String(60), nullable=False, unique=True)
    crud_access = Column(Boolean(), nullable=False)

    employees = relationship("Employee", back_populates="area_table")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer(), primary_key=True)
    category_id = Column(Integer(), ForeignKey('category.id'), nullable=False)
    name = Column(String(60), nullable=False, unique=True)
    model = Column(String(60), nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    quantity = Column(Integer(), nullable=False)

    category_table = relationship("Category", back_populates="products")

class Category(Base):
    __tablename__= "category"

    id = Column(Integer(), primary_key=True)
    name = Column(String(60), nullable=False, unique=True)

    products = relationship("Product", back_populates="category_table")

#Base.metadata.drop_all(engine) #Para borrar la tabla
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()