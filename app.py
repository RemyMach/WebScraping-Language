from manager_picture import ManagerPicture
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from picture import Picture
from scraper_image import ScraperImage
from manager_picture import ManagerPicture
from mlws.mlws import MLWS


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"": {"origins": "http://localhost:port"}})

@app.route('/pictures', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def createPicture():

    # récupérer toute la post request en dict
    picture = request.get_json()
    # convertir le dictionnaire en objet Message
    picture = Picture(picture['name'])

    ScraperImage.imageScrape(picture.name, picture.name)

    return picture.__dict__

@app.route('/pictures/<name>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getPictures(name):

    managerPicture = ManagerPicture(pictures=[])
    managerPicture.setPicturesFromADirectory(name)

    print(managerPicture.pictures)

    return jsonify([picture.__dict__ for picture in managerPicture.pictures])

@app.route('/weblanguage', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def upload_file():
    f = request.files['file']
    directoryName = request.form['directory']
    fileContent = f.read()
    fileContentDecode = fileContent.decode()
    mlws = MLWS(fileContentDecode, directoryName)
    if mlws.validate():
        mlws.parse()
    else:
        return {"Error": "File not recognized"};     
    #f.save(secure_filename(f.filename))
    return {"result": mlws.textOut}

if __name__ == "__main__":
	app.run()