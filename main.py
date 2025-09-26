from flask import Flask
from flask_restful import Api
from application.database import db
from application.model import *
import application.config as config
from application.api.bookcatalogueAPI import BookcatalogueAPI
from application.api.sectionAPI import SectionAPI

app = Flask(__name__)
app.config.from_object(config)
app.app_context().push()
api = Api(app)
db.init_app(app)

api.add_resource(BookcatalogueAPI, '/api/book/<int:book_id>', '/api/book')
api.add_resource(SectionAPI, '/api/section/<int:section_id>', '/api/section')

from application.controller import *
from application.admin_controller import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000, debug=True)