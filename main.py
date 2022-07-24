from flask import Flask,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class Cafe(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(250),unique = True,nullable = False)
    map_url = db.Column(db.String(500),nullable = False)
    img_url = db.Column(db.String(500),nullable = False)
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

#To create table intially
# db.create_all()



@app.route("/data")
def data():
    all_data = db.session.query(Cafe).all()
    cafe_list = [cafe.to_dict() for cafe in all_data]
    return jsonify(cafe = cafe_list)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cafes")
def cafes():
    return render_template("cafes.html")








if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)