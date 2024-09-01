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
    
@app.route("/client")
def client():
    return render_template("client.html")
    
@app.route("/blog")
def blog():
    return render_template("blog.html")
    
@app.route("/book")
def book():
    return render_template("book.html")
    
@app.route("/planNpricing")
def planNpricing():
    return render_template("planNpricing.html")
 
   
@app.route("/ProgramList")
def ProgramList():
    return render_template("ProgramList.html")

@app.route("/contactUs")
def contactUs():
    return render_template("contactUs.html")
    
@app.route("/members")
def members():
    return render_template("members.html")




if __name__ in  "__main__":
    app.run(debug=True)