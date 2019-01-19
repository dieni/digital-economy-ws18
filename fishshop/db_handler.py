from fishshop import db
from fishshop.models import Customer, Product, Producttype


class db_connection:
    '''
    This class handels the connection to the sql database.
    '''

    def create_db(self):
        db.create_all()

        # create some data
        # customer = Customer(cname='testuser', username='sepp', password='seppi69',
        #                     email='seppi@oebb.at', private=True)

        producttype1 = Producttype(
            id=1, producttypename='Fisch', description='Alle Fische')
        product1 = Product(title='Thunfisch', quantity=5,
                           price=100.9, disabled=0, producttype_id='1')

        # Put data into the database
        db.session.add(producttype1)
        db.session.add(product1)
        db.session.commit()

    # def get_customers(self):
    #     customers = db.customer.query.all()
    #     if not customers:
    #         return None
    #     else:
    #         return customers

    def get_products(self):
        return Product.query.all()

        # productobjects = db.product.query.all()
        # if productobjects is None:
        #     return None
        # else:
        #     return productobjects

    # b2c - get all orders
    def get_orders(self, customer_id):
        orderobjects = db.order.query.filter_by(fkkunde=customer_id).all()
        if orderobjects is None:
            return None
        else:
            return orderobjects

    # b2b
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
