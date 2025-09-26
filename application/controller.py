from flask import render_template, request,current_app as app, redirect, url_for, flash, session
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from .admin_controller import searchcatalogue, searchsection
from sqlalchemy import and_, or_
from .model import *
from datetime import date
from datetime import datetime
from datetime import timedelta
from sqlalchemy.sql import func

current_datetime = datetime.now()
currentdate = current_datetime.strftime("%d/%m/%Y")


#---------------- initiallizing login manager-------
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/")
def home():
    
    list=Bookcatalogue.query.order_by(Bookcatalogue.rating.desc()).limit(3)
    
    
    
    return render_template('home.html',list =list)


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        user_mail = request.form["user_mail"]
        password = request.form["password"]
        user = User.query.filter_by(user_mail= user_mail).first()
        if not user:
            flash("you are not registered please register")
            return redirect("/register")
        else:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                
                return redirect("/user_home")
            else:
                flash("please check your password")
                return redirect("/login")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_mail = request.form["user_mail"]
        password = request.form["password"]
        user = User.query.filter_by(user_mail= user_mail).first()
       
        if user:
            flash("user mail already registerd please login")
            return redirect("/login")
        hashed_password= bcrypt.generate_password_hash(password)
        input = User(user_name=user_name, user_mail=user_mail, password=hashed_password)
        db.session.add(input)
        db.session.commit()
        flash("you are now registerd please login")
        return redirect(url_for("login"))


@app.route("/user_home",methods=["GET","POST"])
@login_required
def user_home():
    user=current_user.get_id()
    #print(user)
    current_datetime = datetime.now()
    currentdate = current_datetime.strftime("%d/%m/%Y")
    
    if request.method == "GET":
        books = Bookcatalogue.query.all()
        sections = Section.query.all()
        lend = Bookissue.query.select_from(Bookcatalogue).filter(and_(Bookissue.user_id==user, Bookissue.dateofissue!=0,Bookissue.book_id==Bookcatalogue.book_id,Bookissue.returndate > currentdate)).add_columns(Bookissue.issue_no,Bookcatalogue.book_id,Bookcatalogue.title,Bookcatalogue.book_img_path).all()
        sales = Booksales.query.select_from(Bookcatalogue).filter(and_(Booksales.user_id==user, Booksales.dateofissue!=0,Booksales.book_id==Bookcatalogue.book_id)).add_columns(Booksales.sales_no,Bookcatalogue.book_id,Bookcatalogue.title,Bookcatalogue.book_img_path).all()
        name = User.query.filter_by(user_id=user).first()
        name = name.user_name
        return render_template("user_home.html",books=books,sections=sections,lend=lend,sales=sales,name=name)
    if request.method == "POST":
            user=current_user.get_id()
            data=[]
            sdata=[]          
            try:
                word1=request.form['text']
                head1=request.form['heading']
                data = searchcatalogue(head1,word1)
            except:
                pass
            else:
                pass
            
            try:    
                word2=request.form['stext']
                head2=request.form['sheading']
                sdata = searchsection(head2,word2)
                print(sdata)
            except:
                pass
            else:
                pass
            name = User.query.filter_by(user_id=user).first()
            name = name.user_name
            books = Bookcatalogue.query.all()
            sections = Section.query.all()
            sales = Booksales.query.select_from(Bookcatalogue).filter(and_(Booksales.user_id==user, Booksales.dateofissue!=0,Booksales.book_id==Bookcatalogue.book_id)).add_columns(Booksales.sales_no,Bookcatalogue.book_id,Bookcatalogue.title,Bookcatalogue.book_img_path).all()
            #book=Bookissue.query(user_id=user).all
            lend = Bookissue.query.select_from(Bookcatalogue).filter(and_(Bookissue.user_id==user, Bookissue.dateofissue!=0,Bookissue.book_id==Bookcatalogue.book_id,Bookissue.returndate > currentdate)).add_columns(Bookissue.issue_no,Bookcatalogue.book_id,Bookcatalogue.title,Bookcatalogue.book_img_path).all()
            return render_template('user_home.html',books=books,sections=sections,data=data,sdata=sdata,user=user,lend=lend,sales=sales, name=name)
    
@app.route("/logout_user")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
    
@app.route("/user_request/<book_id>",methods=["GET","POST"])
@login_required
def user_request(book_id):
    user=current_user.get_id()
    #print(user)
    if request.method == "GET":
        book = Bookcatalogue.query.filter_by(book_id=book_id).first()
        count=0
        current_datetime = datetime.now()
        currentdate = current_datetime.strftime("%d/%m/%Y")
        data=Bookissue.query.filter_by(user_id=user).all()
        print(data)
        for record in data: 
            #print(record.returndate)      
            if record.returndate > currentdate:
                count +=1
                #print(count)
        
        if count > 4:
            flash("you have reached your maximum limit.")
            return redirect("/user_home")
        else:
            return render_template("user_request.html",books=book)
    
    if request.method == "POST":
        bookid=request.form['bookid']
    
        action=request.form['option']            
        rating=request.form['rating']

        if float(rating) < 0:
            rating = 0
        elif float(rating) > 5:
            rating = 5
        
        user_id=current_user.get_id()
                
        if action == 'borrow':
            input = Bookissue(book_id=bookid,user_id=user_id,rating=rating,dateofissue=0,returndate=0)
        else:
            input = Booksales(book_id=bookid,user_id=user_id,dateofissue=0)
        db.session.add(input)
        db.session.commit()
        
                
        return redirect('/user_home')
    
@app.route("/surrender/<int:issue_no>", methods=[ "GET", "POST"])
@login_required
def surrender(issue_no):
    book = Bookissue.query.filter_by(issue_no=issue_no).first()
    current_datetime = datetime.now()
    currentdate = current_datetime.strftime("%d/%m/%Y")
    surrender_date = current_datetime - timedelta(days=1)
    surrender_date = surrender_date.strftime("%d/%m/%Y")       
    book.returndate=surrender_date 
    db.session.commit()
    
    return redirect('/user_home')
        
# @app.route("/display_book/<int:book_id>",methods=["GET"])
# def display_book(book_id):
#     if request.method == "GET":
#         book = Bookcatalogue.query.filter_by(book_id=book_id).first()
#         return render_template("display_book.html",book_img_path=book.book_img_path)
    

