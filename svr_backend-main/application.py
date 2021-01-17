import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
#from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'dont tell anyone'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PREFERRED_URL_SCHEME"] = 'https'
app.config["DEBUG"] = False
Session(app)

db = SQL("sqlite:///volunteer.db")
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    #rows = db.execute("SELECT * FROM opportunities")
    return render_template("index.html")

@app.route("/companyregistration", methods = ["GET", "POST"])
def companyregister():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmp = request.form.get("confirm")
        secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
        confirm = bcrypt.generate_password_hash(confirmp).decode('utf-8')
        name = request.form.get("name")
        street = request.form.get("street")
        City = request.form.get("City")
        Country = request.form.get("Country")
        phone = request.form.get("phone")
        website = request.form.get("website")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        jobtitle = request.form.get("jobtitle")
        
        if bcrypt.check_password_hash(secure_password, password):
            db.execute("INSERT INTO companies (name, username, email, password, confirm, street, City, Country, phone, website, firstname, lastname, jobtitle) VALUES (:name, :username, :email, :password, :confirm, :street, :City, :Country, :phone, :website, :firstname, :lastname, :jobtitle)", name=name, username=username, email=email, password=secure_password, confirm=confirm , street=street, City = City, Country=Country, phone=phone, website=website, firstname=firstname, lastname=lastname, jobtitle=jobtitle)
            db.execute("INSERT INTO users (name, username, email, password, confirm) VALUES (:name, :username, :email, :password, :confirm)", name=name, username=username, email=email, password=secure_password, confirm=confirm)
            flash("You are registered and can login", "success")
            return redirect("/login")
        else:     
            flash("password does not match", "danger")  
            return render_template("companyregistration.html")
    return render_template("companyregistration.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmp = request.form.get("confirm")
        secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
        confirm = bcrypt.generate_password_hash(confirmp).decode('utf-8')

        if bcrypt.check_password_hash(secure_password, password):
            db.execute("INSERT INTO users (name, username, email, password, confirm) VALUES (:name, :username, :email, :password, :confirm)", name=name, username=username, email=email, password=secure_password, confirm=confirm)
            flash("You are registered and can login", "success")
            return redirect("/login")
        else:     
            flash("password does not match", "danger")  
            return render_template("register.html")
    return render_template("register.html")

#login
@app.route("/login", methods=["GET","POST"])
def login():
    """Log user in."""
    # forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        session.permanent = True
        username = request.form.get("username")
        password = request.form.get("password")
        # Needs Change here to differ between user and company
        account_type = request.form.get("accounts")
        if account_type == "volunteer":
            usernamedata = db.execute("SELECT username FROM users WHERE username = :username", username=username)
            secure_password = db.execute("SELECT password FROM users WHERE username = :username", username=username)
        else:
            usernamedata = db.execute("SELECT username FROM companies WHERE username = :username", username=username)
            secure_password = db.execute("SELECT password FROM companies WHERE username = :username", username=username)

        # Ensure username was submitted
        if usernamedata is None:
            flash("must provide username", "danger")
            return redirect("/login")
        else:
            # If password == secured_password then go to opportunities
            if bcrypt.check_password_hash(secure_password[0]["password"], password):
                flash("You are now logged in", "success")
                if account_type == "volunteer":
                    return redirect("/opportunities")
                else :
                    return redirect("/post")
            else:
                flash("incorrect password", "danger")
                return redirect("/login")
    else:
        return render_template("login.html")

#Logout
@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect("/login")

#For companies to post new opportunities
@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        companyname = request.form.get("companyname")
        opname = request.form.get("opname")
        daterequired = request.form.get("daterequired")
        description = request.form.get("description")
        skillsgained = request.form.get("skillsgained")
        category =  request.form.getlist("category")
        opcategory = ', '.join(category)

        db.execute("INSERT INTO opportunities (companyname, opname, opcategory, daterequired, description, skillsgained) VALUES (:companyname, :opname, :opcategory, :daterequired, :description, :skillsgained)", companyname=companyname, opname=opname, opcategory=[opcategory], daterequired=daterequired, description=description, skillsgained=skillsgained)
        flash("You posted an opportunity", "success")
        return redirect("/")
    else:
        return render_template("post.html")

@app.route("/opportunities", methods=["GET", "POST"])
def opportunities():
   rows = db.execute("SELECT * FROM opportunities ORDER BY daterequired DESC")
   return render_template("opportunities.html", rows=rows)
    
if __name__ == '__main__':
    app.run(debug = True)