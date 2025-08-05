
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'teknoappsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/teknoapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_or_phone = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email_or_phone = request.form["email_or_phone"]
        password = request.form["password"]
        user = User.query.filter_by(email_or_phone=email_or_phone, password=password).first()
        if user:
            session["user"] = email_or_phone
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="Giriş başarısız.")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
