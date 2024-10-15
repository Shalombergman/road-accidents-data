from flask import Blueprint, jsonify, request

from repository.accidents_repository import get_sum_accidents_by_region, get_accidents_grouped_by_cause, \
    get_injury_statistics_by_region
from repository.csv_repository import init_accident_data
from services.accidents_service import get_accidents_by_period

accidents_blueprint = Blueprint('accidents_blueprint', __name__)

@accidents_blueprint.route('/', methods=['GET'])
def init_db():
    init_accident_data()
    return jsonify({"message": "Database initialized with indexes"}), 201

@accidents_blueprint.route('/accidents/count/<region>', methods=['GET'])
def count_accidents_by_region(region):
    accidents_region = get_sum_accidents_by_region(region)
    return jsonify(accidents_region), 201


@accidents_blueprint.route('/accidents/count/period/', methods=['GET'])
def count_accidents_by_region_and_period():
    data = request.get_json()
    region = data.get('region')
    start_date = data.get('start_date')
    period = data.get('period')


    if not region or not start_date or not period:
        return jsonify({"error": "Missing area, date or period parameter"}), 400

    try:
        accidents_region_period = get_accidents_by_period(region, start_date, period)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(accidents_region_period), 201


@accidents_blueprint.route('/accidents/<region>', methods=['GET'])
def group_accidents_by_cause(region):
    print("jlo;hljjhhh")
    if not region:
        return jsonify({"error": "Region is required"}), 400

    return get_accidents_grouped_by_cause(region)


@accidents_blueprint.route('/accidents/injuries/<region>', methods=['GET'])
def injury_statistics_by_region(region):
    if not region:
        return jsonify({"error": "Region is required"}), 400

    return get_injury_statistics_by_region(region)



