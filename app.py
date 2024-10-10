from flask import Flask

from repository.csv_repository import init_accident_data
from routes.accidents_route import accidents_blueprint

app = Flask(__name__)


app.register_blueprint(accidents_blueprint)


if __name__ == '__main__':

    app.run(debug=True)
