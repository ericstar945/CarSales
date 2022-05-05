from application import app, db
from flask import redirect, render_template, request, flash, url_for, Response, send_file, session
from application.forms import LoginForm, RegisterForm, CarForm, SearchForm
from application.models import User, Car, Favorites
from application.__init__ import fs
from IPython.display import Image
import io
from PIL import Image



def serve_pil_image(pil_img):
    """
    see: 
        https://groups.google.com/forum/?fromgroups=#!topic/python-tornado/B19D6ll_uZE
        http://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser
    """
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)
@app.route("/register", methods = ['GET', 'POST'])
def register():

    if session.get('username'):
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template("register.html", form=form, title="Register an account")
@app.route("/login", methods=['GET', 'POST'])
def login():

    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!","success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, try again!", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/cars", methods = ['GET','POST'])
@app.route("/cars/<carid>")
def cars():
    carData = Car.objects.all()
    return render_template("cars.html", carData=carData)
@app.route("/listcar", methods=['GET', 'POST'])
def listcar():

    if not session.get('username'):
        return redirect(url_for('login'))

    form = CarForm()
    if form.validate_on_submit():
        car_id = Car.objects.count()
        car_id += 1

        make = form.make.data
        model = form.model.data
        description = form.description.data
        year = form.year.data
        price = form.price.data
        phone = form.phone.data
        picture = request.files['picture']
        picture1 = request.files['picture1']
        picture2 = request.files['picture2']
        picname = str(car_id) + "carpic" + year + str(car_id)
        picname1 = str(car_id) + "nextcarpic" + year + str(car_id+1) 
        picname2 = str(car_id) + "lastcarpic" + year + str(car_id+2)
        car = Car(car_id=car_id, make=make, model=model, description=description, year=year, phone=phone, price=price, picname=picname, picname1=picname1, picname2=picname2)
        fs.put(picture, filename=picname)
        fs.put(picture1, filename=picname1)
        fs.put(picture2, filename=picname2)
        car.save()
        flash("Your car is successfully listed!", "success")
        return redirect(url_for('index'))

    return render_template("listcar.html", form=form, title="Create a Listing")
@app.route("/saved", methods=['GET', 'POST'])
def saved():
    if not session.get('username'):
        return redirect(url_for('login'))

    car_id = request.form.get('car_id')
    make = request.form.get('make')
    model = request.form.get('model')
    user_id = session.get('user_id')
    if car_id:
        if Favorites.objects(user_id=user_id, car_id=car_id):
            flash(f"Oops! You have already saved this vehicle: {make} {model}", "danger")
            return redirect(url_for('cars'))
        else:
            Favorites(user_id=user_id, car_id=car_id).save()
            flash(f"You have favorited the {make} {model}", "success")

    cars = list(User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'favorites', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'car', 
                    'localField': 'r1.car_id', 
                    'foreignField': 'car_id', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'car_id': 1
                }
            }
        ]))

    return render_template("saved.html", cars=cars, favorites=True)
@app.route("/carlistings", methods=["GET", "POST"])
def carlistings():
    make = request.form.get('make')
    model = request.form.get('model')
    price = request.form.get('price')
    description = request.form.get('description')
    phone = request.form.get('phone')
    picname = request.form.get('picname')
    picname1 = request.form.get('picname1')
    picname2 = request.form.get('picname2')
    return render_template("carlistings.html", make=make, model=model, price=price, description=description, phone=phone, picname=picname, picname1=picname1, picname2=picname2)
@app.route("/file/<filename>")
def file(filename):
    thing = fs.get_last_version(filename=filename)
    im = Image.open(thing)
    return serve_pil_image(im)

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    user_id = session.get('user_id')
    car_id = request.form.get('car_id')
    picname = request.form.get('picname')
    picname1 = request.form.get('picname1')
    picname2 = request.form.get('picname2')
    Favorites.objects(user_id=user_id, car_id=car_id).delete()
    fs.delete(picname)
    fs.delete(picname1)
    fs.delete(picname2)
    return redirect(url_for('saved'))

@app.route('/about')
def about():
    return render_template("about.html")

    

