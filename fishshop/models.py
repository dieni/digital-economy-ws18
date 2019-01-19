from fishshop import db, login_manager
from flask_login import UserMixin
# UserMixin adds methods like is_authenticated, is_acctive, get_id


@login_manager.user_loader
def load_customer(user_id):
    # reloading user saved in the session
    return Customer.query.get(int(user_id))


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    usertype = db.Column(db.String(20), nullable=False)
    orders = db.relationship('Ordering', backref='customer', lazy=True)

    def __repr__(self):
        '''
        Defines how the user is printed
        '''
        return f"Customer('{self.id}', '{self.cname}', '{self.username}', '{self.password}', '{self.email}'," \
            f"'{self.usertype}',)"


# many to many association between ordering and products
class Association(db.Model):
    ordering_id = db.Column(db.Integer, db.ForeignKey('ordering.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    amount = db.Column(db.Integer)


class Ordering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    finished = db.Column(db.Boolean, default=False)
    canceled = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    payments = db.relationship('Payment', backref='ordering', lazy=True)
    products = db.relationship('Association', backref='ordering', lazy=True)

    def __repr__(self):
        return f"ordering('{self.id}', '{self.finished}', '{self.canceled}','{self.customer_id}')"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fkordering= db.Column(db.Integer, db.ForeignKey('ordering.id'), primary_key=True)
    paymenttype = db.Column(db.String(20))
    fullamount = db.Column(db.Float)
    partialamount = db.Column(db.Float)
    partialpayment = db.Column(db.Boolean, default=False)
    partialquantity = db.Column(db.Integer)
    partialnumber = db.Column(db.Integer)
    fkpartialpayment = db.Column(db.Integer, db.ForeignKey('payment.id'))

    def __repr__(self):
        return f"Payment('{self.id}', '{self.fkordering}', '{self.paymenttype}','{self.fullamount}'," \
            f"'{self.partialamount}','{self.partialpayment}','{self.partialquantity}','{self.partialnumber}'," \
            f" '{self.fkpartialpayment}')"


class Producttype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producttypename = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref="producttype", lazy=True)

    def __repr__(self):
        return f"Producttype('{self.id}', '{self.producttypename}', '{self.description}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    disabled = db.Column(db.Boolean, default=False)
    producttype_id = db.Column(db.Integer, db.ForeignKey('producttype.id'))
    orders = db.relationship('Association', backref='product', lazy=True)

    def __repr__(self):
        return f"Product('{self.id}', '{self.title}', '{self.quantity}', '{self.price}', '{self.disabled}'," \
            f" '{self.producttype_id}')"
