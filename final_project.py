from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantsmenu.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/')
@app.route('/restaurants')
def showRestaurant():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/JSON')
def showRestaurantsJson():
    restaurants= session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurants])


@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantJson(restaurant_id):
    restaurant= session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(Restaurant=restaurant.serialize)

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newItem = Restaurant(name=request.form['name'])
        session.add(newItem)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for('showRestaurant'))
    else:
        return render_template('newrestaurant.html')



@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedItem = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Restaurant Successfully Edited!")

        return redirect(url_for('showRestaurant'))
    else:
    # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
    # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editrestaurant.html', restaurant_id=restaurant_id, item=editedItem)

@app.route('/restaurant/<int:restaurant_id>/delete/',
           methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Restaurant has been deleted!")

        return redirect(url_for('showRestaurant'))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'deleterestaurant.html', restaurant_id=restaurant_id, item=deletedItem)


@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template(
        'menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], desription=request.form[
                           'desription'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created!")

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Menu Item Successfully Edited")

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Menu Item has been Successfully deleted!")

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'deletedItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'supersecret'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
