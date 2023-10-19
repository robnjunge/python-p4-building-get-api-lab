from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries_list = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakeries_list)

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery is None:
        return make_response(jsonify({}), 200)  # Return an empty JSON response with a 200 status code
    bakery_data = bakery.to_dict()
    bakery_data['baked_goods'] = [good.to_dict() for good in bakery.baked_goods]
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods = [baked_good.to_dict() for baked_good in BakedGood.query.order_by(db.desc('price')).all()]
    return jsonify(baked_goods)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(db.desc('price')).first()
    if most_expensive is None:
        return make_response(jsonify({}), 200)  # Return an empty JSON response with a 200 status code
    return jsonify(most_expensive.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)
