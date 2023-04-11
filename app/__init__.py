from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_dropzone import Dropzone
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Luigiman47@localhost/cpsc_449_midterm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '1234'
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'
app.config['DROPZONE_MAX_FILE_SIZE'] = 16  # 16MB
app.config['DROPZONE_UPLOAD_FOLDER'] = 'uploads/images'
CORS(app, resources={r"*": {"origins": "*"}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
dropzone = Dropzone(app)

from app import routes, models, errors


import logging
logging.basicConfig(level=logging.DEBUG)

