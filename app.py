import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SmartDesk.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    image_filename = db.Column(db.String(100))  # Column to store the image filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'kijanamgeni2@gmail.com' and password == 'twendeVasha@2025':
            return 'Welcome to the members Area'
        else:
            return 'Incorrect Email or Password'

@app.route("/blog", methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        date_posted = datetime.strptime(request.form.get('date_posted'), '%Y-%m-%dT%H:%M')
        content = request.form.get('content')

        image = request.files.get('image')
        image_filename = None
        if image and allowed_file(image.filename):
            image_filename = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

        new_post = Blogpost(title=title, author=author, date_posted=date_posted, content=content, image_filename=image_filename)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog'))

    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template("blog.html", posts=posts)

@app.route("/add_blogpost", methods=['GET', 'POST'])
def add_blogpost():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        date_posted = datetime.strptime(request.form.get('date_posted'), '%Y-%m-%dT%H:%M')
        content = request.form.get('content')

        image = request.files.get('image')
        image_filename = None
        if image and allowed_file(image.filename):
            image_filename = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

        new_post = Blogpost(title=title, author=author, date_posted=date_posted, content=content, image_filename=image_filename)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog'))

    return render_template("add_blogpost.html")
@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/ProgramList")
def ProgramList():
    return render_template("ProgramList.html")
    
@app.route("/book")
def book():
    return render_template("book.html")

@app.route("/client")
def client():
    return render_template("client.html")

@app.route("/members")
def members():
    return render_template("members.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/StudentPortal")
def StudentPortal():
    return render_template("StudentPortal.html")

@app.route("/TeachersDashboard")
def TeachersDashboard():
    return render_template("TeachersDashboard.html")

@app.route("/ParentsDashboard")
def ParentsDashboard():
    return render_template("ParentsDashboard.html")


# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
