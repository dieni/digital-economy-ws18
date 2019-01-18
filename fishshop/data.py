from sqlalchemy import create_engine

class db_connection:
    '''
    This class handels the connection to the database.
    '''

    # product dummy
    products = [
        {
            'product_id': 101,
            'title': 'Product 1',
            'price': '30 EUR',
            'available': 999
        },
        {
            'product_id': 102,
            'title': 'Product 2',
            'price': '233 EUR',
            'available': 800
        },
        {
            'product_id': 103,
            'title': 'Product 3',
            'price': '42 EUR',
            'available': 1
        }
    ]

    orders = [
        {
            'order_id': 201,
            'customer_id': 301,
            'payment_id': '',
            'products': [
                {
                    'product_id': 101,
                    'quantity': 1
                },
                {
                    'product_id': 102,
                    'quantity': 2
                }
            ],
            'bought': True,
            'canceled': False
        },
        {
            'order_id': 202,
            'customer_id': 301,
            'payment_id': '',
            'products': [
                {
                    'product_id': 101,
                    'quantity': 1
                }
            ],
            'bought': True,
            'canceled': False
        },
        {
            'order_id': 203,
            'customer_id': 302,
            'payment_id': '',
            'products': [
                {
                    'product_id': 102,
                    'quantity': 2
                }
            ],
            'bought': False,
            'canceled': False
        }
    ]

    customers = [
        {
            'customer_id': 301,
            'password': 'password',
            'private': False
        },
        {
            'customer_id': 302,
            'password': 'password',
            'private': True
        }
    ]

    def get_products(self):
        '''
        Get a list of all products
        '''
        # TODO link with database
        return self.products

    def get_orders(self, customer_id):
        '''
        Get all orders from a customer
        '''
        customer_orders = []
        for o in self.orders:
            if o['customer_id'] == customer_id:
                customer_orders.append(o)

        return customer_orders

    def search_product(self, id):
        # TODO search in database
        return "specific product"

    def cancel_order(self, customer_id, order_id):
        '''
        cancel an order from a user
        '''
        for o in self.orders:
            if o['customer_id'] == customer_id and o['order_id'] == order_id:
                o['canceled'] = True
                return 'Cancelled'

        return 'Wrong order id'

    def authorize(self, username, password):
        '''
        Check if a username with this password exsits. If yes, return the user else return None (null)
        '''

        for c in self.customers:
            if c['customer_id'] == username and c['password'] == password:
                return c

        return None
