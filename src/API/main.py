from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello_world():
    return "arrrr matey!"

if __name__ == "__main__":
    app.run(debug=True)
