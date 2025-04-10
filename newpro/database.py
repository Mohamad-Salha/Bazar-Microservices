from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import datetime

Base = declarative_base()

# Define Book model for catalog service
class Book(Base):
    __tablename__ = 'books'
    
    item_number = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(100), nullable=False)
    stock = Column(Integer, default=0)
    cost = Column(Integer, nullable=False)
    
    def to_dict(self):
        return {
            'item_number': self.item_number,
            'title': self.title,
            'topic': self.topic,
            'stock': self.stock,
            'cost': self.cost
        }

# Define Order model for order service
class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(String(36), primary_key=True)
    item_number = Column(Integer, nullable=False)
    timestamp = Column(String(50), default=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'item_number': self.item_number,
            'timestamp': self.timestamp
        }

# Database utility functions
def get_db_engine(service_name):
    """Create a database engine for the specified service"""
    # Use SQLite for simplicity, can be replaced with other databases in production
    db_path = f'{service_name}.db'
    return create_engine(f'sqlite:///{db_path}')

def get_db_session(engine):
    """Create a database session"""
    Session = sessionmaker(bind=engine)
    return Session()

def init_db(engine):
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(engine)

def import_books_from_csv(session, csv_file):
    """Import books data from CSV file to database"""
    import csv
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            book = Book(
                item_number=int(row['item_number']),
                title=row['title'],
                topic=row['topic'],
                stock=int(row['stock']),
                cost=int(row['cost'])
            )
            session.add(book)
        session.commit()

def import_orders_from_csv(session, csv_file):
    """Import orders data from CSV file to database"""
    import csv
    try:
        with open(csv_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                order = Order(
                    order_id=row['order_id'],
                    item_number=int(row['item_number']),
                    timestamp=row['timestamp']
                )
                session.add(order)
            session.commit()
    except FileNotFoundError:
        # It's okay if the orders file doesn't exist yet
        pass