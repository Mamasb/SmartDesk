from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/signup")
def signup():
    return render_template("signup.html")
    
@app.route("/login")
def login():
    return render_template("login.html")
    
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


if __name__ in  "__main__":
    app.run(debug=True)