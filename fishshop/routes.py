from flask import Flask, render_template, url_for, request, Response, flash, redirect, session
from fishshop import app, db, bcrypt
from fishshop.forms import LoginForm
from fishshop.models import Customer, Ordering, Product, Producttype, Payment
from flask_login import login_user, current_user, logout_user, login_required
from fishshop.db_handler import db_connection

# from fishshop.models import Customer
# from fishshop import db

import xml.etree.ElementTree as et


db_con = db_connection()


# B2C Webshop


@app.route('/')
@app.route('/home')
def home():
    '''
    This is the start page of our webshop.
    '''

    return render_template('home.html', title='Home', authorized=checkSession())


@app.route('/dbcreate')
def dbcreate():
    '''
    This is the start page of our webshop.
    '''
    db_con.create_db()

    return 'Database created'


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page so the use can login to the system. Get session for a user
    '''

    # if user is already logged in redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        # check if there is a customer with this id
        customer = Customer.query.filter_by(
            username=form.username.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check id and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/products')
def products():
    '''
    Here the user can see all products which are available.
    '''
    # TODO: Modify the template to check some products to buy. Use a Button to proceed with purchasing.
    # products = db_con.get_products()  # get products from the database
    products = Product.query.all()  # get products from the database

    if not products:
        return 'None'

    return render_template('products.2.html', title='Products', products=products, authorized=checkSession())



@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():

    if request.method == 'POST':

        # get chosen products from form

        products = Product.query.filter_by(disabled=False).all()

        products_in_cart = []
        for p in products:
            if int(request.form[str(p.id)]) > 0:
                p.quantity = int(request.form[str(p.id)])
                products_in_cart.append(p)

        return render_template('cart.html', title='Cart', products=products_in_cart)

    return redirect(url_for('products'))


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    '''
    C2B
    '''

    #customer = Customer.query.filter_by(id=current_user.id).first()

    if request.method == 'POST':

        count = 0

        buy = []
        for p in request.form.get('quantity'):
            count += 1
            product = Product.query.find_by(title=p['ptitle']).first()
            product.quantity = p['quantity']
            buy.append(product)

        return "Thank you for your order " + str(count)


@app.route('/dashboard')
def dashboard():
    '''
    If a user is logged in, he or she can manage the orders here. If the user is an admin the user has additional
    functions.

    UC: storno / administration
    '''
    return "dashboard"


# B2B Webshop
# Here the EDI is implemented. All methods must have some authorization mechanism.

@app.route('/api/products')
def api_products():
    '''
    Get a list of all Products
    '''

    # query the products
    products = Product.query.all()

    # building xml
    root = et.Element('products')

    for p in products:
        product = et.SubElement(root, 'product')
        product_id = et.SubElement(product, 'id')
        product_id.text = str(p.id)
        title = et.SubElement(product, 'title')
        title.text = str(p.title)
        available = et.SubElement(product, 'quantity')
        available.text = str(p.quantity)
        price = et.SubElement(product, 'price')
        price.text = str(p.price)
        price = et.SubElement(product, 'disabled')
        price.text = str(p.disabled)
        price = et.SubElement(product, 'producttype_id')
        price.text = str(p.producttype_id)

    xml_str = et.tostring(root, encoding='utf8', method='xml')

    return Response(xml_str, mimetype='text/xml')


@app.route('/api/search', methods=['GET', 'PUT'])
def api_search():
    # TODO
    if request.method == 'PUT':
        return "XML with list of search results"
    else:
        # Return schema of search
        return 'Schema'


@app.route('/api/orders', methods=['GET', 'PUT', 'POST'])
def cancellation():
    '''

    Customer must be authorized.


    PUT: Cancel a specific order
    POST: Order a product
    GET: Get a list of all orders of a user
    '''
    # Authorization
    customer = authorize(request.authorization.username,
                         request.authorization.password)

    if not customer:
        return 'You are not authorized'
    if request.method == 'PUT':
        # cancel order and send back confirmation.

        root = et.fromstring(request.data)

        # get order id from request
        bestellung_ids = root.findall(".//bestellungid")  # returns a list
        bestellung_id = int(bestellung_ids[0].text)

        # storno
        result = db_con.cancel_ordering(bestellung_id)
        if result != -1:
            root = et.Element('storno')
            bestell_id = et.SubElement(root, 'bestellungid')
            storno = et.SubElement(root, 'storniert')
            bestell_id.text = str(bestellung_id)
            storno.text = "erfolgreich"
            xml_str = et.tostring(root, encoding='utf8', method='xml')
        else:
            return "Order nicht gefunden!"

    elif request.method == 'POST':
        # reading the xml from the request
        root = et.fromstring(request.data)

        # get order id from request
        product_ids = root.findall(".//produktid")  # returns a list
        product_id = int(product_ids[0].text)

        amounts = root.findall(".//menge")  # returns a list
        amount = int(amounts[0].text)

        # insert new ordering and return new ordering id
        ordering_id = db_con.create_ordering(product_id, customer.id, amount)

        if ordering_id != -1:
            root = et.Element('kauf')
            bestell_id = et.SubElement(root, 'bestellungid')
            bestell_id.text = str(ordering_id)

            xml_str = et.tostring(root, encoding='utf8', method='xml')

            return Response(xml_str, mimetype='text/xml')
        else:
            return "Ware nicht vorhanden!"

    else:
        # return a list of orders from a user
        orders = db_con.get_orders(customer['customer_id'])

        # building xml
        root = et.Element('orders')

        for o in orders:
            order = et.SubElement(root, 'order')
            order_id = et.SubElement(order, 'id')
            order_id.text = str(o['order_id'])
            customer_id = et.SubElement(order, 'customer_id')
            customer_id.text = str(o['customer_id'])
            payment_id = et.SubElement(order, 'payment_id')
            payment_id.text = str(o['payment_id'])

            # build all products in an order
            products = et.SubElement(order, 'products')
            for p in o['products']:
                product = et.SubElement(products, 'product')
                product_id = et.SubElement(product, 'product_id')
                product_id.text = str(p['product_id'])
                quantity = et.SubElement(product, 'quantity')
                quantity.text = str(p['quantity'])

            bought = et.SubElement(order, 'bought')
            bought.text = str(o['bought'])
            canceled = et.SubElement(order, 'canceled')
            canceled.text = str(o['canceled'])

    # creating from a string
    xml_str = et.tostring(root, encoding='utf8', method='xml')

    return Response(xml_str, mimetype='text/xml')


def authorize(username, password):
    '''
    This is a method to authorize a customer. If login is missing or is wrong response with error message will sent. Else this
    method returns the customer object.
    '''

    customer = Customer.query.filter_by(username=username).first()
    if customer and bcrypt.check_password_hash(customer.password, password):
        return customer
    else:
        return None


def checkSession():
    '''
    This method checks if a session exists
    '''
    if 'customer' in session:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)
