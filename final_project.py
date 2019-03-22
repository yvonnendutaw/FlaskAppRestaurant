from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurant():
    #Fake Restaurants

    restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

    restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
    #Fake Menu Items
    items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
    item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new')
def newRestaurant():
    return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
    restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
    for i in restaurants:
        if (restaurant.get('id')) is None:
                restaurant_id = restaurant.get('id')
                editedItem = restaurant.get("name", "")
                return render_template('editrestaurant.html',restaurant_id=restaurant_id, item=editedItem)
        else:
                restaurant_id = restaurant.get('id')

                return render_template('norestaurant.html',restaurant_id=restaurant_id)




@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu():
    return "This page is for creating restaurant_id/menu"


@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant():
    return "This page deletes an existing restaurant"


@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenu():
    return "This page is for creating restaurant_id/menu"


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenu():
    return "This page is for editing restaurant_id/menu_id"

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenu():
    return "This page is for editing restaurant_id/menu_id"



if __name__ == '__main__':
    app.secret_key = 'supersecret'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
