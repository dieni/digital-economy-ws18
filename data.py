class db_connection:
    '''
    This class handels the connection to the database.
    '''

    # product dummy
    products = [
        {
            'product_id': 123,
            'title': 'Product 1',
            'price': '30 EUR',
            'available': 999
        },
        {
            'product_id': 112,
            'title': 'Product 2',
            'price': '233 EUR',
            'available': 800
        },
        {
            'product_id': 666,
            'title': 'Product 3',
            'price': '42 EUR',
            'available': 1
        }
    ]

    def get_products(self):
        '''
        Get a list of all products
        '''
        return self.products
