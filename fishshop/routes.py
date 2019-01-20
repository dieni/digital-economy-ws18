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

customer_cart = {}

# B2C Webshop


@app.route('/')
@app.route('/home')
def home():
    '''
    This is the start page of our webshop.
    '''

    # , authorized=checkSession())
    return render_template('home.html', title='Home')


@app.route('/dbcreate')
def dbcreate():
    '''
    This is the start page of our webshop.
    '''
    db_con.create_db()

    return 'Database created'

# c2b storno


@app.route('/storno')
def storno():
    '''
    This is the page for ordering storno
    '''

    orderobjects = Ordering.query.filter_by(customer_id=4).filter_by(
        canceled=False).filter_by(finished=False).all()
    if not orderobjects:
        return 'None'
    # , authorized=checkSession())
    return render_template('storno.html', title='Orders', orders=orderobjects)


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


@app.route('/manage/login', methods=['GET', 'POST'])
def loginAdmin():
    '''
    Login page so the use can login to the system. Get session for a user
    '''

    # if user is already logged in redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('administration'))

    form = LoginForm()

    if form.validate_on_submit():
        # check if there is a admin with this id
        admin = Customer.query.filter_by(
            username=form.username.data).first()
        if admin and admin.usertype == 'Admin' and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('administration'))
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

    # , authorized=checkSession())
    return render_template('products.2.html', title='Products', products=products)


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():

    if request.method == 'POST':

        # get chosen products from form

        products = Product.query.filter_by(disabled=False).all()

        # products_in_cart = []
        customer_cart[current_user.id] = []
        for p in products:
            if p.quantity > 0:
                if int(request.form[str(p.id)]) > 0:
                    p.quantity = int(request.form[str(p.id)])
                    # products_in_cart.append(p)
                    customer_cart[current_user.id].append(p)

        return render_template('cart.html', title='Cart', products=customer_cart[current_user.id])

    return redirect(url_for('products'))


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    '''
    C2B
    '''

    #customer = Customer.query.filter_by(id=current_user.id).first()

    if request.method == 'POST':

        # current user
        current_user

        # products purchaised
        products = customer_cart[current_user.id]

        # payment method
        payment_method = str(request.form['payment_method'])

        # number of payments
        payments = str(request.form['quantity_payments'])

        # write to database
        if db_con.buy_products(current_user.id, products, payment_method, payments):
            return "Thank you for your order!"

        return "Something went wrong. Please try again later."


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


@app.route('/api/search', methods=['GET', 'PUT', 'POST'])
def api_search():
    # TODO
    if request.method == 'PUT':
        return "XML with list of search results"
    else:
        if request.method == 'GET':
            #TODO
            return "Get"
        else:
            if request.method == 'POST':
                httpxml = et.fromstring(request.data)
                
                # building xml
                root = et.Element('products')
                
                for pr in httpxml.findall("produktid"):
                    p = db_con.search_product(int(pr.text))
                    
                    if p is None:
                        continue

                    product = et.SubElement(root, 'product')
                    product_id = et.SubElement(product, 'id')
                    product_id.text = str(p.id)
                    title = et.SubElement(product, 'title')
                    title.text = str(p.title)
                    price = et.SubElement(product, 'price')
                    price.text = str(p.price)
                    available = et.SubElement(product, 'disabled')
                    available.text = str(p.disabled)
                
                xml_str = et.tostring(root, encoding='utf8', method='xml')
                # Return schema of search
                return Response(xml_str, mimetype='text/xml')



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
            storno.text = 'erfolgreich'
            xml_str = et.tostring(root, encoding='utf8', method='xml')
            return Response(xml_str, mimetype='text/xml')
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

    '''
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
'''

#Admin Area
@app.route('/manage/admin', methods=['GET', 'PUT', 'POST'])
def administration():

    #admin = authorizeAdmin(request.authorization.username, request.authorization.password)
    #if not admin:
    #    return 'You are not authorized'
    products = Product.query.all()

    if request.method == 'GET' and current_user.usertype == 'Admin':
        return render_template('admin.html', title='Adminstrator Page', products=products)
    else:
        return 'Sorry you dont have admin rights'


@app.route('/manage/updateproduct', methods=['GET', 'PUT', 'POST'])
@login_required
def update_product():

    if request.method == 'POST':

        # get all products
        products = Product.query.all()
 
        for p in products:
            #DeActivate product
            if request.form[str(p.id)] == 'True' and p.disabled == 0:
                productobject = Product.query.filter_by(id=p.id).first()
                productobject.disabled = True
                db.session.commit()
                

            #Activate product
            if request.form[str(p.id)] == 'False' and p.disabled == 1:                 
                 productobject = Product.query.filter_by(id=p.id).first()
                 productobject.disabled = False
                 db.session.commit()

        return render_template('admin.html', title='Administration Page', products=products, status="update")

    return redirect(url_for('administration'))

    
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



# def checkSession():
#     '''
#     This method checks if a session exists
#     '''
#     if 'customer' in session:
#         return True
#     else:
#         return False


if __name__ == '__main__':
    app.run(debug=True)
