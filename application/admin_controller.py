from flask import render_template, request,current_app as app, redirect, url_for, flash, session
from .model import Bookcatalogue, Section, Bookissue, Booksales, User, db
from sqlalchemy.sql import func
from datetime import date
from datetime import datetime
from datetime import timedelta
from sqlalchemy import and_, or_

current_datetime = datetime.now()
currentdate = current_datetime.strftime("%d/%m/%Y")

def searchcatalogue (heading, text):
    if heading == 'title':
        data = Bookcatalogue.query.filter(Bookcatalogue.title.like('%{}%'.format(text))).all()
        return data
    elif heading == 'publisher':
        data = Bookcatalogue.query.filter(Bookcatalogue.publisher.like('%{}%'.format(text))).all()
        return data
    elif heading == 'authorfname':
        data = Bookcatalogue.query.filter(Bookcatalogue.authorfname.like('%{}%'.format(text))).all()
        return data
    
    elif heading == 'section':
        data = Bookcatalogue.query.filter(Bookcatalogue.section.like('%{}%'.format(text))).all()
        return data
    else:
        return []
    
def searchsection (heading, text):
    if heading == 'name':
        data = Section.query.filter(Section.name.like('%{}%'.format(text))).all()
        return data
    elif heading == 'description':
        data = Section.query.filter(Section.description.like('%{}%'.format(text))).all()
        return data
    else:
        return []
  

def bookavailable():
    current_datetime = datetime.now()
    currentdate = current_datetime.strftime("%d/%m/%Y")
    books = Bookcatalogue.query.all()
    bookissued = Bookissue.query.all()
    bookdic={}
    for issued in bookissued:
        if issued.returndate> currentdate:
            if issued.book_id in bookdic:
                bookdic[issued.book_id] +=1
            else:
                bookdic[issued.book_id] =1
            
    for record in bookdic:                
        for list in books:                    
            if list.book_id == int(record):
                list.copies = list.copies-bookdic[record]
    return books            
                        


@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    if request.method == "POST":
        email= request.form["user_mail"]
        password = request.form["password"]
        if (email == 'admin@gmail.com' and password == "1234"):
            session['email'] = email
            return redirect('/admin')
        else:
            flash("you are not allowed to see admin functions.")
            return redirect('/login')

@app.route("/admin", methods=["GET","POST"])
def admin_dashboard():
    if ('email' in session):
        email_in_session = session["email"]
        if request.method == "GET":
            
            sections = Section.query.all()
            sales = Booksales.query.select_from(Bookcatalogue).filter(and_(Booksales.user_id==User.user_id, Booksales.dateofissue==0,Booksales.book_id==Bookcatalogue.book_id)).add_columns(Booksales.sales_no, User.user_id,User.user_name,Bookcatalogue.book_id,Bookcatalogue.title).all()
            lend = Bookissue.query.select_from(Bookcatalogue).filter(and_(Bookissue.user_id==User.user_id, Bookissue.dateofissue==0,Bookissue.book_id==Bookcatalogue.book_id)).add_columns(Bookissue.issue_no, User.user_id,User.user_name,Bookcatalogue.book_id,Bookcatalogue.title).all()
            books=bookavailable()    
            issuedbooks = Bookissue.query.select_from(Bookcatalogue).filter(and_(Bookissue.user_id==User.user_id, Bookissue.returndate> currentdate,Bookissue.book_id==Bookcatalogue.book_id)).add_columns(Bookissue.issue_no, User.user_id,User.user_name,Bookcatalogue.book_id,Bookcatalogue.title).all()
            
            return render_template('admin.html',books=books,sections=sections,lend=lend, issuedbooks=issuedbooks,sales=sales)
        
        if request.method == "POST":
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
                
            except:
                pass
            else:
                pass


            books = bookavailable()
            sections = Section.query.all()
            lend = Bookissue.query.select_from(Bookcatalogue).filter(and_(Bookissue.user_id==User.user_id, Bookissue.dateofissue==0,Bookissue.book_id==Bookcatalogue.book_id)).add_columns(Bookissue.issue_no, User.user_id,User.user_name,Bookcatalogue.book_id,Bookcatalogue.title).all()
            issuedbooks = Bookissue.query.select_from(Bookcatalogue).filter(and_(Bookissue.user_id==User.user_id, Bookissue.returndate> currentdate,Bookissue.book_id==Bookcatalogue.book_id)).add_columns(Bookissue.issue_no, User.user_id,User.user_name,Bookcatalogue.book_id,Bookcatalogue.title).all()
            sales = Booksales.query.select_from(Bookcatalogue).filter(and_(Booksales.user_id==User.user_id, Booksales.dateofissue==0,Booksales.book_id==Bookcatalogue.book_id)).add_columns(Booksales.sales_no, User.user_id,User.user_name,Bookcatalogue.book_id,Bookcatalogue.title).all()

            return render_template('admin.html',books=books,sections=sections,data=data,sdata=sdata,lend=lend,issuedbooks=issuedbooks,sales=sales)
    else:
        flash("you are not allowed to see admin functions.")
        return redirect('/login')

@app.route("/logoutAdmin")
def logoutAdmin():
    if ('email' in session):
        session.pop('email',None)
        return redirect('/login')
    else:
        flash("you are not allowed to see admin function")
        return redirect('/login')

@app.route("/add_section", methods=["GET","POST"])
def add_section():
    if ('email' in session):
        email_in_session = session["email"]
        if request.method == "GET":
            return render_template("add_section.html")
        if request.method == "POST":
            print("hello")
            secname = request.form["name"]
            date = request.form["date"]
            desc = request.form["describe"]

            input = Section(name=secname, date_created=date,description =desc)
            db.session.add(input)
            db.session.commit()
            return redirect('/admin')
    else:
        flash("you are not allowed to see admin functions.")
        return redirect('/login')


@app.route("/add_book", methods=["GET","POST"])
def add_book():
    if ('email' in session):
        email_in_session = session["email"]
        if request.method == "GET":
            sections = Section.query.all()
            return render_template("add_book.html",sections=sections)
        if request.method == "POST":
            
            booktitle = request.form["bookname"]
            aufname = request.form["afname"]
            aulname = request.form["alname"]
            publish = request.form["publis"]
            year = request.form["year"]
            section = request.form["section"]
            cont = request.form["content"]
            copy = request.form["copies"]
            book_rapper = request.files["book_rapper"]
            book_rapper.save('static/'+ book_rapper.filename)
            book_img_path = str("./static/"+book_rapper.filename)

            input = Bookcatalogue(title=booktitle, authorfname=aufname,authorlname=aulname, publisher = publish, year=year,section = section, content = cont, copies = copy, book_img_path = book_img_path)
            db.session.add(input)
            db.session.commit()
            return redirect('/admin')
    else:
        flash("you are not allowed to see admin functions.")
        return redirect('/login')
    
@app.route("/edit_section/<section_id>", methods=["GET","POST"])
def edit_section(section_id):
    if request.method == "GET":
        section = Section.query.filter_by(section_id=section_id).first()
        return render_template("edit_section.html", section=section)
    if request.method == "POST":
        section = Section.query.filter_by(section_id=section_id).first()
        section.name = request.form["name"]
        section.date_created = request.form["date"]
        section.description = request.form["describe"]
        
        db.session.commit()
        return redirect('/admin')

@app.route("/edit_book/<book_id>",methods=['GET', 'POST'])
def edit_book(book_id):
    if request.method == "GET":
        book = Bookcatalogue.query.filter_by(book_id=book_id).first()
       
        return render_template("edit_book.html",book=book)
    if request.method == "POST":
       
        book = Bookcatalogue.query.filter_by(book_id=book_id).first()
        book.title = request.form["bookname"]
        book.authorfname = request.form["afname"]
        book.authorlname = request.form["alname"]
        book.publisher = request.form["publis"]
        book.year = request.form["year"]
        book.section = request.form["section"]
        book.content = request.form["content"]
        book.copies = request.form["copies"]
        book_rapper = request.files["book_rapper"]
        book_rapper.save('static/'+ book_rapper.filename)
        book.book_img_path = str("./static/"+book_rapper.filename)        
        
        db.session.commit()
        return redirect('/admin')



@app.route("/dlt_book/<int:book_id>")
def dlt_book(book_id):
    book = Bookcatalogue.query.filter_by(book_id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('/admin')

@app.route("/dlt_section/<int:section_id>")
def dlt_section(section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    db.session.delete(section)
    db.session.commit()
    return redirect('/admin')

@app.route("/search_book", methods=["GET", "POST"])
def search_book():
    if request.method == "GET":
        return render_template("search_book.html")
    if request.method == "POST":
       word=request.form['text']
       head=request.form['heading']
       data = searchcatalogue(head,word)

       books = Bookcatalogue.query.all()
       sections = Section.query.all()
       return render_template('admin.html',books=books,sections=sections,data=data)
    
@app.route("/display_book/<int:book_id>",methods=["GET"])
def display_book(book_id):
    if request.method == "GET":
        book = Bookcatalogue.query.filter_by(book_id=book_id).first()
        return render_template("display_book.html",book_img_path=book.book_img_path)

@app.route("/updaterating", methods=[ "GET", "POST"])
def updaterating():
    rate = db.session.query(Bookissue.book_id,func.avg(Bookissue.rating)).group_by(Bookissue.book_id).all()
    
    for avg in rate:
        bookid=avg[0]
        rate = avg[1]
        try:
            book = Bookcatalogue.query.filter_by(book_id=bookid).first()
            book.rating = round(rate,2)
            db.session.commit()
        except:
            pass
        else:
            pass

        
    return redirect('/admin')

@app.route("/approve_lend/<int:issue_no>", methods=[ "GET", "POST"])

def approve_lend(issue_no):
    book = Bookissue.query.filter_by(issue_no=issue_no).first()

    current_datetime = datetime.now()
    currentdate = current_datetime.strftime("%d/%m/%Y")
    due_date = current_datetime + timedelta(days=7)
    due_date = due_date.strftime("%d/%m/%Y")    
    book.dateofissue=currentdate 
    book.returndate=due_date
    db.session.commit()
    
    return redirect('/admin')

@app.route("/reject_lend/<int:issue_no>", methods=[ "GET", "POST"])
def reject_lend(issue_no):
    book = Bookissue.query.filter_by(issue_no=issue_no).first()      
    book.dateofissue='Rejected' 
    db.session.commit()
    
    return redirect('/admin')

@app.route("/revoke/<int:issue_no>", methods=[ "GET", "POST"])
def revoke(issue_no):
    book = Bookissue.query.filter_by(issue_no=issue_no).first()
    current_datetime = datetime.now()
    currentdate = current_datetime.strftime("%d/%m/%Y")
    surrender_date = currentdate - timedelta(days=1)
    surrender_date = surrender_date.strftime("%d/%m/%Y")       
    book.returndate=surrender_date 
    db.session.commit()
    
    return redirect('/admin')


@app.route("/approve_sell/<int:sales_no>", methods=[ "GET", "POST"])
def approve_sell(sales_no):
    book = Booksales.query.filter_by(sales_no=sales_no).first()
    book.dateofissue=currentdate     
    db.session.commit()
    
    return redirect('/admin')

@app.route("/reject_sell/<int:sales_no>", methods=[ "GET", "POST"])
def reject_sell(sales_no):
    book = Booksales.query.filter_by(sales_no=sales_no).first()      
    book.dateofissue='Rejected' 
    db.session.commit()
    
    return redirect('/admin')    

       
