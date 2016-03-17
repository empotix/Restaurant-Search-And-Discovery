from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem, Reviews

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
restaurant1 = Restaurant(name="Dominos Pizza")

session.add(restaurant1)
session.commit()

menuItem2 = MenuItem(name="Margherita Pizza", description="Single Cheese Topping",
                     price="$7.50", course="Entree", restaurant=restaurant1)

session.add(menuItem2)
session.commit()


menuItem1 = MenuItem(name="Peporoni Pizza", description="100% Pork Peporoni",
                     price="$8.99", course="Entree", restaurant=restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name="Garlic Bread", description="Comes along with Cheesy Dip",
                     price="$3.50", course="Appetizer", restaurant=restaurant1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="Chocolate Cake", description="Fresh baked and served with ice cream",
                     price="$3.99", course="Dessert", restaurant=restaurant1)

session.add(menuItem3)
session.commit()

menuItem5 = MenuItem(name="Root Beer", description="16oz of refreshing goodness",
                     price="$1.99", course="Beverage", restaurant=restaurant1)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(name="Iced Tea", description="with Lemon",
                     price="$.99", course="Beverage", restaurant=restaurant1)

session.add(menuItem6)
session.commit()

review1 = Reviews(name = "Gaurav Keswani", restaurant = restaurant1, review = '''This Domino's pizza in Powai is doing great from handling crowd to good service all I faced is 1 problem that it's conjugated and no proper seats arrangements.
																					Pizza lovers can hangout here as you will find many other pizza stores next to domino's 
																					Value for money - 3.5/5
																					Ambiance 3.5/5
																					Service 4/5
																					Food quality and quantity 3.5/5
																					Hygiene 3.5/5
																					Taste 4/5''' )
session.add(review1)
session.commit()

review2 = Reviews(name = "Vishesh Shah", restaurant = restaurant1, review = '''Just like any other dominos outlet. I had to go with my all time favourite panner and onion. This time I tried the zingy parcel and it was totally OK. The veg parcel was a treat with little panner cubes and cream flowing out though it, but the non veg parcel was too hard to chew and tasted like uncooked dough!!! Definately not something worthing going on for the second time!!! But the panner and onion pizza never fails to amaze me... Its cheesey , its tasty and its very low on the pocket!!!! 
Do try on the veg. Parcel my fellow foodies!!!!''' )
session.add(review2)
session.commit()

review3 = Reviews(name = "Saurabh Rawool", restaurant = restaurant1, review = '''This is in the Hiranandani business park close to a plethora of offices. Though I am not a pizza lover, went one day for a farewell party. The shop is too small for any dominos outlet and gives a instant feeling that it has been setup to cater deliveries for all the offices around.

The seats are usual with no ambience whatsoever. Just a glass house to do business. As far the pizza is concerned, I did not find it even to dominos standard which in itself is falling. It was just dry to say the least.The person doing the billing screwed up the bill as well. There was 30pc discount and we asked for a 10 pc corporate discount which they happily agreed upon. When the bill came, it was just 10pc and the 30 percent discount vanished. We asked once , they admitted the mistake and informed once bill is done , its irreversible. We did not pursue. The service was okay-ish.

Overall i don't like dominos pizza but still get some delivered when in groups. It was a mistake visiting the store it seems. And this store did not make things better. Being in such a prime location, they should know how to handle clients or just run a delivery outlet. 

Will not visit again but then again sometimes you have to being a part of a group. If you want a cheap office party just go to galleria. Lots of option at half the price and healthy food at the same time.''' )
session.add(review3)
session.commit()

review4 = Reviews(name = "Smit Sawant", restaurant = restaurant1, review = '''
Home delivery is very fast. Prices of almost all food items are as per standards. Can apply various coupons (check offers regularly) while ordering online.''' )
session.add(review4)
session.commit()




