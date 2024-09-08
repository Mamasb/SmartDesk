import os
from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SmartDesk.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

db = SQLAlchemy(app)

# Define your models
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    image_filename = db.Column(db.String(100))  # Column to store the image filename

class Employee(db.Model):
    __tablename__ = 'emp'
    empid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = get_current_user()
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'kijanamgeni2@gmail.com' and password == 'twendeVasha@2025':
            return 'Welcome to the members Area'
        else:
            error = 'Incorrect Email or Password'
    return render_template('login.html', loginerror=error, user=user)

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

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'db'):
        g.db.close()

def get_current_user():
    return session.get('user')

@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        existing_user = User.query.filter_by(name=name).first()
        if existing_user:
            return render_template('register.html', registererror='Username already taken, try a different username.')
        new_user = User(name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', user=user)

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    emp_records = Employee.query.all()
    return render_template('dashboard.html', user=user, allemp=emp_records)

@app.route('/addnewemployee', methods=["POST", "GET"])
def addnewemployee():
    user = get_current_user()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        new_employee = Employee(name=name, email=email, phone=phone, address=address)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewemployee.html', user=user)

@app.route('/singleemployee/<int:empid>')
def singleemployee(empid):
    user = get_current_user()
    emp_record = Employee.query.get(empid)
    return render_template('singleemployee.html', user=user, single_emp=emp_record)

@app.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_current_user()
    emp_record = Employee.query.get(empid)
    return render_template('updateemployee.html', user=user, single_emp=emp_record)

@app.route('/updateemployee', methods=["POST", "GET"])
def updateemployee():
    user = get_current_user()
    if request.method == 'POST':
        empid = request.form['empid']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        emp_record = Employee.query.get(empid)
        if emp_record:
            emp_record.name = name
            emp_record.email = email
            emp_record.phone = phone
            emp_record.address = address
            db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('updateemployee.html', user=user)

@app.route('/deleteemp/<int:empid>', methods=["GET", "POST"])
def deleteemp(empid):
    user = get_current_user()
    if request.method == 'GET':
        emp_record = Employee.query.get(empid)
        if emp_record:
            db.session.delete(emp_record)
            db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
