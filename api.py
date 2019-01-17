from flask import Flask, render_template, url_for, request, Response

from data import db_connection
import xml.etree.ElementTree as et

app = Flask(__name__)
app.config['SECRET_KEY'] = '24446f27d7e8540adcaf914f0aea6bd7'


db = db_connection()

# B2C Webshop


@app.route('/')
@app.route('/home')
def home():
    '''
    This is the start page of our webshop.
    '''
    return render_template('home.html', title='Home')


@app.route('/login')
def login():
    '''
    Login page so the use can login to the system. Get session for a user
    '''
    return render_template('login.html', title='Login')


@app.route('/products')
def products():
    '''
    Here the user can see all products which are available.
    '''
    # TODO: Modify the template to check some products to buy. Use a Button to proceed with purchasing.
    products = db.get_products()  # get products from the database
    return render_template('products.html', title='Products', products=products)


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

    products = db.get_products()

    # building xml
    root = et.Element('products')

    for p in products:
        product = et.SubElement(root, 'product')
        product_id = et.SubElement(product, 'id')
        product_id.text = str(p['product_id'])
        title = et.SubElement(product, 'title')
        title.text = str(p['title'])
        price = et.SubElement(product, 'price')
        price.text = str(p['price'])
        available = et.SubElement(product, 'available')
        available.text = str(p['available'])

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


@app.route('/api/orders', methods=['GET', 'PUT'])
def cancellation():
    '''
    FINISHED
    Customer must be authorized.

    GET: Get a list of all orders of a user
    PUT: Cancel a specific order
    '''
    # Authorization
    customer = authorize(request)

    if request.method == 'PUT':
        # cancel order and send back confirmation.

        # reading the xml from the request
        root = et.fromstring(request.data)

        # get order id from request
        order_id = root.findall(".//bestellungid")  # returns a list

        # cancel order
        return db.cancel_order(customer['customer_id'], int(order_id[0].text))

    else:
        # return a list of orders from a user
        orders = db.get_orders(customer['customer_id'])

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


def authorize(request):
    '''
    This is a method to authorize a customer. If login is missing or is wrong response with error message will sent. Else this
    method returns the customer object.
    '''
    auth = request.authorization

    if not auth:
        return "You are not authorized!"

    customer = db.authorize(int(auth.username), auth.password)

    if not customer:
        return "Wrong customer id or password!"

    # if authorization is ok return object of customer
    return customer


if __name__ == '__main__':
    app.run(debug=True)
