from .database import db


class User(db.Model):
    __table_name__ = "user"
    user_id =  db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(30),  nullable = False)
    user_mail = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(30), nullable = False)
    is_active =db.Column(db.Boolean)

    bookcatalogue = db.relationship('Bookissue', back_populates = 'user')
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    

class Section(db.Model):
    __tablename__ = 'section'
    section_id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable = False)    
    date_created = db.Column(db.String(), nullable = False)
    description = db.Column(db.String(), nullable = False)

    
   
class Bookcatalogue(db.Model):
    __tablename__ = 'bookcatalogue'
    book_id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    title = db.Column(db.String(), nullable = False)
    authorfname = db.Column(db.String(), nullable = False)
    authorlname = db.Column(db.String())
    publisher = db.Column(db.String(), nullable = False)
    year = db.Column(db.Integer(), nullable = False)
    section = db.Column(db.String(),db.ForeignKey("section.name"), nullable = False)
    copies = db.Column(db.Integer(), nullable = False)
    content = db.Column(db.String(), nullable = False)
    rating = db.Column(db.Float, default = 0)
    book_img_path = db.Column(db.String())

    user = db.relationship('Bookissue',back_populates = 'bookcatalogue')
    

class Bookissue(db.Model):
    __tablename__ = 'bookissue'
    issue_no = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.user_id"), nullable = False)
    book_id = db.Column(db.String(),db.ForeignKey("bookcatalogue.book_id"), nullable = False)
    rating = db.Column(db.Float, default = 0)
    dateofissue = db.Column(db.String())
    returndate = db.Column(db.String())

    bookcatalogue = db.relationship("Bookcatalogue", back_populates = "user")
    user = db.relationship('User', back_populates = 'bookcatalogue')

class Booksales(db.Model):
    __tablename__ = 'booksales'
    sales_no = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.user_id"), nullable = False)
    book_id = db.Column(db.Integer(),db.ForeignKey("bookcatalogue.book_id"), nullable = False)
    dateofissue = db.Column(db.String())