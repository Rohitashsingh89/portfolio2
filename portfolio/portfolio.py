from flask import Flask, render_template, url_for, request, redirect,session
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.utils import secure_filename
from flask_mail import Mail
import json
from datetime import datetime
import os 
import math

with open('config.json', 'r') as j:
    parameters = json.load(j)['parameters']

local_server = True
app = Flask(__name__) 

app.secret_key = "Hello"
app.config['UPLOAD_FOLDER'] = parameters['upload_location']

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = parameters['gmail_user'],
    MAIL_PASSWORD = parameters['gmail_password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = parameters['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameters['production_url']

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    # date = db.Column(db.String(20), nullable=False)
    date = datetime.now()


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    tagline = db.Column(db.String(200), nullable=False)
    # date = db.Column(db.String(20), nullable=False)
    date = datetime.now()


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('index.html', parameters=parameters)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        Message = request.form['msg']
        entry = Contact(name=name, email=email, phone_num=phone, msg=Message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                        sender = email, 
                        recipients = [parameters['gmail_user']],
                        body = Message + "\n" + phone
                        )
   
    return render_template("contact.html", parameters=parameters)


@app.route("/blog")
def blog():
    post = Posts.query.filter_by().all()
    last = math.ceil(len(post) / int(parameters['no_of_posts'] ))
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1

    page = int(page)
    # slicing
    post = post[(page -1) * int(parameters['no_of_posts']) : (page -1) * int(parameters['no_of_posts']) + int(parameters['no_of_posts'])]
    # pagination logic
    # STARTING
    if page == 1:
        prev = "#"
        next = "/?page=" +str(page + 1)
    # LAST
    elif page == last:
        prev = "/?page=" +str(page - 1)
        next = "#"
    # MIDDLE
    else:
        prev = "/?page=" +str(page - 1)
        next = "/?page=" +str(page + 1)
    
    # slug is unique
    return render_template('blog.html', parameters=parameters, post=post, prev=prev, next=next)
    
@app.route("/post/<string:post_slug>", methods = ['GET'] )
def post_route(post_slug):
    # slug is unique
    post = Posts.query.filter_by().all() [0 : parameters['no_of_posts']]
    return render_template('blog.html', parameters=parameters, post=post)
    
# @app.route("/qrgenerator/", methods = ['GET'] )
# def qrgenerator(post_slug):
#     # slug is unique
#     post = Posts.query.filter_by(post_slug=post_slug).first()
#     return render_template('blog.html', parameters=parameters, post=post)
    

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if ('user' in session and session['user'] == parameters['admin_user']):
        post = Posts.query.all()
        return render_template('dashboard.html', parameters=parameters, post=post)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpassword = request.form.get('password')
        if(username == parameters['admin_user'] and userpassword == parameters['admin_password']):
            # set the session variable
            session['user'] = username
            post = Posts.query.all()
            return render_template('dashboard.html', parameters=parameters, post=post)
    else:
        return render_template('login.html', parameters=parameters)
    
@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if ('user' in session and session['user'] == parameters['admin_user']):
        if request.method == 'POST':
            e_title = request.form.get('title')
            e_tline = request.form.get('tline')
            e_slug = request.form.get('slug')
            e_content = request.form.get('content')
            # e_img_file = request.form.get('img_file')
            date = datetime.now()

            if sno == '0':
                post = Posts(title=e_title, slug=e_slug, content=e_content, tagline=e_tline, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = e_title
                post.slug = e_slug
                post.content = e_content
                post.tagline = e_tline
                post.date = date
                db.session.commit()
                return redirect('/edit/'+sno)

        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', parameters=parameters, post=post)
        
@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if ('user' in session and session['user'] == parameters['admin_user']):
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')
    
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route("/signup")
def signup():
    return render_template('signup.html', parameters=parameters)
    
@app.route("/python")
def python():
    return render_template('python.html', parameters=parameters)
    
@app.route("/pandas")
def pandas():
    return render_template('pandas.html', parameters=parameters)
    
@app.route("/numpy")
def numpy():
    return render_template('numpy.html', parameters=parameters)
    
@app.route("/ml", methods=['GET', 'POST'])
def ML():
    post = Posts.query.filter_by().all()        
    return render_template('ML.html', parameters=parameters, post=post)
    
# login 
@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html', parameters=parameters)


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if ('user' in session and session['user'] == parameters['admin_user']):
        if (request.method == 'POST'):
            ufile = request.files['file']
            ufile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ufile.filename)))
            return "Uploaded successfully"

    
@app.route("/about")
def about():
    return render_template('about.html', parameters=parameters)
    

if __name__ == "__main__":
    from portfolio import db, app
    
    with app.app_context():
        db.create_all()
        app.run(debug=True)
