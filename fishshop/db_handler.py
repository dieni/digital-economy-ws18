from fishshop import db
from fishshop.models import Customer


class db_connection:
    '''
    This class handels the connection to the sql database.
    '''

    def create_db(self):
        db.create_all()

        # create some data
        customer = Customer(cname='testuser', username='sepp', password='seppi69',
                            email='seppi@oebb.at', private=True)

        # Put data into the database
        db.session.add(customer)
        db.session.commit()

        return Customer.query.all()

    def get_products(self):
        productobjects = db.product.query.all()
        if productobjects is None:
            return None
        else:
            return productobjects

    #b2c - get all orders
    def get_orders(self, customer_id):
        orderobjects = db.order.query.filter_by(fkkunde=customer_id).all()
        if orderobjects is None:
            return None
        else:
            return orderobjects

    #b2b
    def search_product(self, id):
        productobject = db.product.query.filter_by(id=id).first()
        if productobject is None:
            return None
        if productobject.disabled == 0:
            return None
        else:
            return productobject.quantity

    #b2b and b2c
    def cancel_order(self, order_id, db):
        orderobject = db.order.query.filter_by(id=order_id).first()
        if orderobject is None:
            return None
        else:
            orderobject.canceled = 1
            db.session.add(orderobject)
            db.session.commit()
            return True



    def authorize(self, username, password):
        '''
        Check if a username with this password exsits. If yes, return the user else return None (null)
        '''
        pass
