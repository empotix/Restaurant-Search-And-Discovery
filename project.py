from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, Reviews

#Creating an instance of the flask application
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response

import httplib2
import json

app = Flask(__name__)

#Creating the session with the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Decorator that wraps our function inside the route function that
#flask has already created. If either of '/' or '/' gets sent from
#the browser, this function gets executed
@app.route('/')
def landing_page():
	return render_template('cover.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route('/display_restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('index.html', restaurants = restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
def show_restaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	reviews = session.query(Reviews).all()
	return render_template('restaurant_home.html', restaurant = restaurant, reviews = reviews)


@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurant_menu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant = restaurant, items = menu_items)

#By default, a route in flask only responds to GET requests. We need to add the
#method parameter to make it respond to POST requests
@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):

	#If we have come here via a form, it means we have already submitted the new
	#menu item. Else, we have come here to see the form where we will enter the
	#menu item
	if request.method == 'POST':
		item = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(item)
		session.commit()
		flash("New menu item has been created")
	 	return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
	else:
	 	return render_template('new_menu_item.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	if request.method == 'POST':
		item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
		item.name = request.form['new_name']
		session.add(item)
		session.commit()
		flash("New menu item has been edited")
	 	return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
	else:
		item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
		return render_template('edit_menu_item.html', restaurant_id = restaurant_id, menu_id = menu_id, current = item.name)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	if request.method == 'POST':
		item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
		session.delete(item)
		session.commit()
		flash("New menu item has been deleted")
	 	return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
	else:
		item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
		return render_template('delete_menu_item.html', restaurant_id = restaurant_id, menu_id = menu_id, current = item.name)

#Making an endpoint for a JSON GET request
@app.route('/restaurants/<int:restaurant_id>/menu/json/')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return jsonify(MenuItems = [i.serialize for i in menu_items])

#Making an endpoint for a JSON GET request
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/menu/json/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu_item = session.query(MenuItem).filter_by(id = menu_id, restaurant_id = restaurant_id).one()
	return jsonify(MenuItems = menu_item.serialize)

@app.route('/restaurants/<int:restaurant_id>/review', methods = ['GET', 'POST'])
def addReview(restaurant_id):
	if request.method == 'GET':
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		return render_template('add_review.html', restaurant = restaurant )

if __name__ == "__main__":
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
