from fishshop import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    private = db.Column(db.Boolean)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        '''
        Defines how the user is printed
        '''
        return f"Customer('{self.id}', '{self.username}', '{self.email}', '{self.password}')"


# many to many association between order and products
association_table = db.Table('association_order_product',
                             db.Column('order_id', db.Integer,
                                       db.ForeignKey('order.id'), primary_key=True),
                             db.Column('product_id', db.Integer,
                                       db.ForeignKey('product.id'), primary_key=True)
                             )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    finished = db.Column(db.Boolean, default=False)
    canceled = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    products = db.relationship(
        'Product', secondary=association_table, lazy='subquery', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"Order('{self.id}', '{self.finished}', '{self.canceled}')"


class Payment():
    pass


class Producttype():
    pass


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    disabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Product('self.id', 'self.title', 'self.quantity', 'self.price', 'self.disabled')"
