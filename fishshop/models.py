from fishshop import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    private = db.Column(db.Boolean)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        '''
        Defines how the user is printed
        '''
        return f"Customer('{self.id}', '{self.name}', '{self.username}', '{self.password}', '{self.email}'," \
            f"'{self.private}',)"


# many to many association between order and products
association_table = db.Table('association_order_product',
                             db.Column('order_id', db.Integer,
                                       db.ForeignKey('order.id'), primary_key=True),
                             db.Column('product_id', db.Integer,
                                       db.ForeignKey('product.id'), primary_key=True),
                             db.Column('amount', db.Integer)
                             )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    finished = db.Column(db.Boolean, default=False)
    canceled = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    payments = db.relationship('Payment', backref='order', lazy=True)
    products = db.relationship(
        'Product', secondary=association_table, lazy='subquery', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"Order('{self.id}', '{self.finished}', '{self.canceled}','{self.customer_id}')"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fkorder = db.Column(db.Integer, db.ForeignKey, primary_key=True)
    paymenttype = db.Column(db.String(20))
    fullamount = db.Column(db.Float)
    partialamount = db.Column(db.Float)
    partialpayment = db.Column(db.Boolean, default=False)
    partialquantity = db.Column(db.Integer, nullable=False)
    partialnumber = db.Column(db.Integer, nullable=False)
    fkpartialpayment = db.Column(db.Integer, db.ForeignKey('payment.id'))

    def __repr__(self):
        return f"Payment('{self.id}', '{self.fkorder}', '{self.paymenttype}','{self.fullamount}'," \
            f"'{self.partialamount}','{self.partialpayment}','{self.partialquantity}','{self.partialnumber}'," \
            f" '{self.fkpartialpayment}')"


class Producttype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producttypename = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref="product", lazy=True)

    def __repr__(self):
        return f"Producttype('{self.id}', '{self.producttypename}', '{self.description}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    disabled = db.Column(db.Boolean, default=False)
    producttype_id = db.Column(db.Integer, db.ForeignKey('Producttype.id'))

    def __repr__(self):
        return f"Product('{self.id}', '{self.title}', '{self.quantity}', '{self.price}', '{self.disabled}'," \
            f" '{self.producttype_id}')"


