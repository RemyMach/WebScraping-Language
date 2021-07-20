from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from picture import Picture

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"": {"origins": "http://localhost:port"}})


@app.route('/pictures', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
# Message message
def createPicture():

    # récupérer toute la post request en dict
    picture = request.get_json()
    # convertir le dictionnaire en objet Message
    picture = Picture(picture)

    return picture.__dict__

if __name__ == "__main__":
	app.run()