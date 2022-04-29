from application import app, db
from flask import redirect, render_template, request

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)
@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/cars", methods = ['GET','POST'])
@app.route("/cars/<carid>")
def cars():
    carData = [{"carID":"1111","make":"GMC","model":"Sierra","description":"Great truck, low miles","year":"2012","price":"$15,000"},{"carID":"2222","make":"Fiat","model":"500","description":"Kind of a car","year":"2011","price":"$10,000"}]
    return render_template("cars.html", carData=carData)
@app.route("/listcar")
def listcar():
    return render_template("listcar.html")
@app.route("/saved", methods=["GET", "POST"])
def saved():
    make = request.form.get('make')
    model = request.form.get('model')
    price = request.form.get('price')
    return render_template("saved.html", make=make, model=model, price=price)
@app.route("/carlistings", methods=["GET", "POST"])
def carlistings():
    make = request.form.get('make')
    model = request.form.get('model')
    price = request.form.get('price')
    description = request.form.get('description')

    return render_template("carlistings.html", make=make, model=model, price=price, description=description)

class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)

@app.route("/user")
def user():
    #User(user_id=1, first_name="Eric", last_name="Greilich", email="ericstar999@gmail.com", password="123456").save()
    #User(user_id=2, first_name="Ricky", last_name="Allen", email="ricky@gmail.com", password="123456").save()
    users = User.objects.all()
    return render_template("user.html", users=users)