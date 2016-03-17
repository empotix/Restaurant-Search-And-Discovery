# For creating a database with SQL Alchemy, there are 4 major components:
# 1. Configuration: used to import the necessary modules and binds the code to the SQL Alchemy engine
#                    Also creates an instance of the declarative base and connects to the database/ create a new one
# 2. Class: used to represent data in python
# 3. Table: represents the table in the database
# 4. Mapper: connects columns of the database to the class that reprsents it

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#Lets SQL Alchemy know that our classes are special SQL alchemy classes 
#that correspond to table in the database
Base = declarative_base() 

class Restaurant(Base):
    
    #Table information
    __tablename__ = 'restaurant'
    
    #Mapper information
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    
    #Table information
    __tablename__ = 'menu_item'
    
    #Mapper information
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    
    #Returns object data in serializable format
    @property
    def serialize(self):
        return {
            'name' : self.name,
            'description' : self.description,
            'price' : self.price,
            'course' : self.course,
        }

class Reviews(Base):

    #Table information
    __tablename__ = 'reviews'

    #Mapper information
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    review = Column(String(1000), nullable = False)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

#Goes into the database and adds all the classes as new tables
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)