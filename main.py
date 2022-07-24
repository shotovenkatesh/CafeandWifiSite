from flask import Flask,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "ssdfasvixrctvuoyibhjnkmefgeqbfqefcqechqfc"

class Cafe(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(250),unique = True,nullable = False)
    map_url = db.Column(db.String(500),nullable = True)
    img_url = db.Column(db.String(500),nullable = True)
    location = db.Column(db.String(250),nullable = False)
    has_sockets = db.Column(db.Boolean,nullable = False)
    has_toilet = db.Column(db.Boolean,nullable = False)
    has_wifi = db.Column(db.Boolean,nullable = False)
    can_take_calls = db.Column(db.Boolean,nullable = False)
    seats = db.Column(db.String(250),nullable = False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

class Form(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    location = StringField("Location",validators=[DataRequired()])
    sockets = BooleanField("Sockets",validators=[DataRequired()])
    toilets = BooleanField("Toilets")
    wifi = BooleanField("Wifi")
    calls = BooleanField("Calls")
    seats = StringField("Seats",validators=[DataRequired()])
    coffee_price = StringField("Coffee Price",validators=[DataRequired()])
    submit = SubmitField("submit")

#To create table intially
# db.create_all()



# @app.route("/data",methods = ["GET"])
# def data():
#     all_data = db.session.query(Cafe).all()
#     cafe_list = [cafe.to_dict() for cafe in all_data]
#     print(cafe_list)
#     return jsonify(cafe = cafe_list)

all_data = db.session.query(Cafe).all()
cafe_list = [cafe.to_dict() for cafe in all_data]
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cafes")
def cafes():
    return render_template("cafes.html",cafe_data = cafe_list)

@app.route("/add",methods = ["GET","POST"])
def add():
    form =Form()
    if form.validate_on_submit():
        name = form.name.data
        location = form.location.data
        sockets = form.sockets.data
        toilets = form.toilets.data
        wifi = form.wifi.data
        calls = form.calls.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        map_url = "random url of a location"
        img_url = "img url "
        new_cafe_data = Cafe(name = name,
                             map_url = map_url,
                             img_url = img_url,
                             location = location,
                             has_sockets = sockets,
                             has_toilet = toilets,
                             has_wifi = wifi,
                             can_take_calls = calls,
                             seats = seats,
                             coffee_price = coffee_price)
        db.session.add(new_cafe_data)
        db.session.commit()
        return render_template("cafes.html")
    return render_template("add.html",form = form)






if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)