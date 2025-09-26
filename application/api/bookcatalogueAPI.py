from flask_restful import Resource, marshal_with, abort,fields,reqparse
from flask import  jsonify

from application.model import Bookcatalogue, db

resource_fields={
    "book_id": fields.Integer,
    "title":fields.String,
    "authorfname": fields.String,
    "authorlname": fields.String,
    "publisher":fields.String,
    "year":fields.Integer,
    "section":fields.String,
    "copies":fields.Integer,
    "content":fields.String,
    "rating":fields.Float
    
}

bookcatalogue_post_args = reqparse.RequestParser()
bookcatalogue_post_args.add_argument('title', type=str, required = True, help="book name is not here")
bookcatalogue_post_args.add_argument('authorfname', type = str, required = True, help="author name is not here")
bookcatalogue_post_args.add_argument('authorlname', type = str)
bookcatalogue_post_args.add_argument('publisher', type = str, required = True, help="publisher is not here")
bookcatalogue_post_args.add_argument('year', type = int, required = True, help="year name is not here")
bookcatalogue_post_args.add_argument('section', type = str, required = True, help="section name is not here")
bookcatalogue_post_args.add_argument('copies', type = int, required = True, help="copies name is not here")
bookcatalogue_post_args.add_argument('content', type = str, required = True, help="content name is not here")
bookcatalogue_post_args.add_argument('rating', type = float, required = True, help="rating name is not here")


bookcatalogue_put_args = reqparse.RequestParser()
bookcatalogue_put_args.add_argument('title', type=str)
bookcatalogue_put_args.add_argument('authorfname', type = str)
bookcatalogue_put_args.add_argument('authorlname', type = str)
bookcatalogue_put_args.add_argument('publisher', type = str)
bookcatalogue_put_args.add_argument('year', type = int)
bookcatalogue_put_args.add_argument('section', type = str)
bookcatalogue_put_args.add_argument('copies', type = int)
bookcatalogue_put_args.add_argument('content', type = str)
bookcatalogue_put_args.add_argument('rating', type = float)




class BookcatalogueAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        book = Bookcatalogue.query.filter_by(book_id=book_id).first()
        if not book:
            return abort(404,message="book does\'t exist")
        return book, 200


    def post(self):
        args = bookcatalogue_post_args.parse_args()
        input = Bookcatalogue(title = args['title'], authorfname = args['authorfname'], authorlname =args['authorlname'] , publisher  = args['publisher'], year  = args['year'], section  = args['section'], copies  = args['copies'], content  = args['content'], rating = args['rating'])
        db.session.add(input)
        db.session.commit()
        return jsonify({'status':'success', 'message':'data is added'})


    def delete(self,book_id):
        book = Bookcatalogue.query.filter_by(book_id=book_id).first()
        if not book:
            return abort(404,message="book does\'t exist")
        db.session.delete(book)
        db.session.commit()
        return jsonify({'status':'success', 'message':'book deleted'})

    @marshal_with(resource_fields)
    def put(self, book_id):
        args = bookcatalogue_put_args.parse_args()
        book = Bookcatalogue.query.filter_by(book_id=book_id).first()
        if not book:
            return abort(409,message="book is not exist" )
        if args['title']:
            book.title_name = args['title']
        if args['authorfname']:
            book.authorfname = args['authorfname']
        if args['authorlname']:
            book.authorlname = args['authorlname']
        if args['publisher']:
            book.publisher = args['publisher']
        if args['year']:
            book.year = args['year']
        if args['section']:
            book.section = args['section']
        if args['copies']:
            book.copies = args['copies']
        if args['content']:
            book.copies = args['content']
        if args['rating']:
            book.copies = args['rating']
        
        db.session.commit()
        return book, 200







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