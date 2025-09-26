from flask_restful import Resource, marshal_with, abort,fields,reqparse
from flask import  jsonify

from application.model import Section, db

resource_fields={
    "section_id": fields.Integer,
    "name":fields.String,
    "date_created": fields.String,
    "description": fields.String
    
}

section_post_args = reqparse.RequestParser()
section_post_args.add_argument('name', type=str, required = True, help="section name is not here")
section_post_args.add_argument('date_created', type = str, required = True, help="Date of creation is not here")
section_post_args.add_argument('description',type = str, required = True, help="description is not here")



section_put_args = reqparse.RequestParser()
section_put_args.add_argument('name', type=str)
section_put_args.add_argument('date_created', type = str)
section_put_args.add_argument('description', type = str)





class SectionAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, section_id):
        section = Section.query.filter_by(section_id=section_id).first()
        if not section:
            return abort(404,message="section does\'t exist")
        return section, 200


    def post(self):
        args = section_post_args()
        input = Section(name = args['name'], date_created = args['date_created'], description =args['description'])
        db.session.add(input)
        db.session.commit()
        return jsonify({'status':'success', 'message':'data is added'})


    def delete(self,section_id):
        section = Section.query.filter_by(book_id=book_id).first()
        if not section:
            return abort(404,message="section does\'t exist")
        db.session.delete(section)
        db.session.commit()
        return jsonify({'status':'success', 'message':'section deleted'})

    @marshal_with(resource_fields)
    def put(self, section_id):
        args = section_put_args.parse_args()
        section = Section.query.filter_by(section_id=section_id).first()
        if not section:
            return abort(409,message="section is not exist" )
        if args['name']:
            section.name = args['name']
        if args['date_created']:
            section.date_created = args['date_created']
        if args['authorlname']:
            section.description = args['description']    
        
        db.session.commit()
        return section, 200







# {
#     "title":"Advance MAD",
#     "authorfname": "delhi",
#     "authorlname":"chandni chowk",
#     "publisher":"publisher",
#     "year":2024,
#     "section":"Health"  
#     "copies":5, 
#     "content":"how a web application can be developed",
#     "rating":2.5
# }