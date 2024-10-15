from flask import Flask

from repository.accidents_repository import get_accidents_grouped_by_cause
from repository.csv_repository import init_accident_data
from routes.accidents_route import accidents_blueprint

app = Flask(__name__)


app.register_blueprint(accidents_blueprint)


if __name__ == '__main__':
    get_accidents_grouped_by_cause(225)
    app.run(debug=True)
