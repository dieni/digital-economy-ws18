from fishshop import db, bcrypt
from fishshop.models import Customer, Product, Producttype, Ordering, Payment, Association


class db_connection:
    # This class handels the connection to the sql database.

    def create_db(self):
        db.create_all()

        # Insert Customer
        # the first user = admin
        customer1 = Customer(cname='Admin', username='admin',
                             password=bcrypt.generate_password_hash(
                                 'password').decode('UTF-8'),
                             email='admin@customer.at', usertype='Admin')
        customer2 = Customer(cname='Hans Jackson', username='private1',
                             password=bcrypt.generate_password_hash(
                                 'password').decode('UTF-8'),
                             email='jackson@customer.at', usertype='Private')
        customer3 = Customer(cname='Otto Bolt', username='private2',
                             password=bcrypt.generate_password_hash(
                                 'password').decode('UTF-8'),
                             email='bolt@customer.at', usertype='Private')
        customer4 = Customer(cname='Firma Merkur', username='business1',
                             password=bcrypt.generate_password_hash(
                                 'password').decode('UTF-8'),
                             email='merkur@customer.at', usertype='Business')
        customer5 = Customer(cname='Firma Billa', username='business1',
                             password=bcrypt.generate_password_hash(
                                 'password').decode('UTF-8'),
                             email='billa@customer.at', usertype='Business')
        # Put data into the database
        db.session.add(customer1)
        db.session.add(customer2)
        db.session.add(customer3)
        db.session.add(customer4)
        db.session.add(customer5)

        # Insert Dummy ordering
        ordering = Ordering(finished=False, canceled=False, customer_id=1)
        # Put data into the database
        db.session.add(ordering)

        # Insert Dummy Payment
        payment = Payment(id=1, fkordering=1, paymenttype="dummy", fullamount=0.0, partialamount=0.0, partialpayment=True,
                          partialquantity=0, partialnumber=0, fkpartialpayment=1)
        # Put data into the database
        db.session.add(payment)

        # Insert Producttype
        producttype1 = Producttype(
            producttypename='Fisch', description='Alle Fische')
        producttype2 = Producttype(
            producttypename='Muscheln', description='Alle Muscheln')
        producttype3 = Producttype(
            producttypename='Krebstiere', description='Alle Krebstiere')
        producttype4 = Producttype(producttypename='Sonstige', description='Sonstige Produkte wie '
                                                                           'zb. Aufstriche, Olivenöl etc.')
        # Put data into the database
        db.session.add(producttype1)
        db.session.add(producttype2)
        db.session.add(producttype3)
        db.session.add(producttype4)

        # Insert Product
        product1 = Product(title='Thunfisch', quantity=45,
                           price=100.34, disabled=0, producttype_id='1')
        product2 = Product(title='Lachs', quantity=86,
                           price=59.90, disabled=0, producttype_id='1')
        product3 = Product(title='Schwertfisch', quantity=10,
                           price=200.23, disabled=0, producttype_id='1')
        product4 = Product(title='Miesmuschel', quantity=160,
                           price=10.98, disabled=0, producttype_id='2')
        product5 = Product(title='Jacobsmuschel', quantity=5,
                           price=60.22, disabled=0, producttype_id='2')
        product6 = Product(title='Venusmuschel', quantity=76,
                           price=13.78, disabled=0, producttype_id='2')
        product7 = Product(title='Krabbe', quantity=71,
                           price=50.25, disabled=0, producttype_id='3')
        product8 = Product(title='Garnele', quantity=20,
                           price=10.34, disabled=0, producttype_id='3')
        product9 = Product(title='Hummer', quantity=98,
                           price=1000.25, disabled=0, producttype_id='3')
        product10 = Product(title='Olivenöl', quantity=0,
                            price=8.90, disabled=1, producttype_id='4')

        # Put data into the database
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.add(product4)
        db.session.add(product5)
        db.session.add(product6)
        db.session.add(product7)
        db.session.add(product8)
        db.session.add(product9)
        db.session.add(product10)

        # Insert association_table
        association = Association(ordering_id=1, product_id=1, amount=1)

        # Put data into the database
        db.session.add(association)

        # commit all inserts
        db.session.commit()

    # test Methods for get all tables
    def get_all_customer(self):
        return Customer.query.all()

    def get_all_ordering(self):
        return Ordering.query.all()

    def get_all_payment(self):
        return Payment.query.all()

    def get_all_producttype(self):
        return Producttype.query.all()

    def get_all_products(self):
        return Product.query.all()

    def get_all_association(self):
        return Association.query.all()

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
