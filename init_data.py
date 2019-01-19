from fishshop import app, db
from fishshop.models import Customer, Order, Payment, Producttype, Product

if __name__ == '__main__':
    app.run(debug=True)

    print('yay')
    # createinitial dabase
    db.create_all()

    # create some data
    customer = Customer(name='testuser', username='sepp',
                        email='seppi@oebb.at', private=True)

    # Put data into the database
    db.session.add(customer)
    db.session.commit()

    # Query the data
    print(Customer.query.all())
