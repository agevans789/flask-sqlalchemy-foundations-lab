# server/app.py
#!/usr/bin/env python3

from flask_migrate import Migrate
from flask import Flask, make_response, jsonify
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthquake:
        body = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }
        return make_response(body, 200)
    else:
        body = {'message': f'Earthquake {id} not found.'}
        return make_response(body, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    # Query all earthquakes with magnitude greater than or equal to the input
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Structure the list for the response
    quakes_data = []
    for q in quakes:
        quakes_data.append({
            "id": q.id,
            "magnitude": q.magnitude,
            "location": q.location,
            "year": q.year
        })
    
    # Return the dictionary with count and quakes list
    response_dict = {
        "count": len(quakes_data),
        "quakes": quakes_data
    }
    
    return make_response(jsonify(response_dict), 200)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
