from sqlalchemy import create_engine  # for what is this import?


class db_connection:
    '''
    This class handels the connection to the sql database.
    '''

    def get_products(self):
        '''
        Get a list of all products
        '''
        # TODO link with database
        pass

    def get_orders(self, customer_id):
        '''
        Get all orders from a customer
        '''
        pass

    def search_product(self, id):
        # TODO search in database
        pass

    def cancel_order(self, customer_id, order_id):
        '''
        cancel an order from a user
        '''
        pass

    def authorize(self, username, password):
        '''
        Check if a username with this password exsits. If yes, return the user else return None (null)
        '''
        pass
