from flask import Blueprint, request, jsonify

from vytals import db
from vytals.exceptions import InvalidUsage
from vytals.models import Reading, User
from vytals.utils import parse_reading, reading_validator

reading = Blueprint('reading', __name__)


@reading.route('/readings/user/<int:id>/new', methods=['POST'])
def create_reading(id: int):
    if not reading_validator.validate(request.json):
        raise InvalidUsage(reading_validator.errors, status_code=404)

    reading = parse_reading(request.json)
    user = User.query.filter_by(id=id).first()

    if user is None:
        raise InvalidUsage("There is no user associated with the id provided.", status_code=404)

    reading.user_id = user.id
    db.session.add(reading)
    db.session.commit()

    return jsonify(reading=reading.serialize()), 201


@reading.route('/readings/user/<int:id>/all', methods=['GET'])
def get_readings(id: int):
    readings = Reading.query.filter_by(user_id=id).all()

    if len(readings) == 0:
        raise InvalidUsage("There are no readings associated with the id provided.", status_code=404)

    return jsonify(readings=[r.serialize() for r in readings]), 200
