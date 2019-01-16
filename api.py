from flask import Flask, render_template, url_for, request, Response

from data import db_connection
import xml.etree.ElementTree as et

app = Flask(__name__)
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
    products = db.get_products

    # return "products"
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
    # TODO
    if request.method == 'PUT':
        # cancel order and send back confirmation.
        return "confirmation"
    else:
        # return a list of orders from a user
        return "List of order"


if __name__ == '__main__':
    app.run(debug=True)
