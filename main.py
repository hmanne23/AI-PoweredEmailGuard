from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
import os
import re
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=10)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class EmailHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email_text = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.Integer, nullable=False)   # Important: Integer!
    confidence = db.Column(db.Float, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load the models
pipe = pickle.load(open("Naive_model.pkl", "rb"))
data = pd.read_csv("emails.csv")
X = data['text'].values
y = data['spam'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
cv = CountVectorizer()
X_train_cv = cv.fit_transform(X_train)
svm = SVC(probability=True)
svm.fit(X_train_cv, y_train)

def is_secure_password(password):
    return (len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[^A-Za-z0-9]', password))

@app.route("/")
def home():
    if not current_user.is_authenticated:
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for("login"))
    return redirect(url_for("classify"))

@app.route("/classify", methods=["GET", "POST"])
@login_required
def classify():
    if request.method == "POST":
        text = request.form.get("email", "").strip()
        model_choice = request.form.get("model", "naive_bayes")
        if not text:
            return render_template("show.html", prediction="No input provided.", confidence=None)

        if model_choice == "naive_bayes":
            output = int(pipe.predict([text])[0])  # 🛡️ Forcefully int
            confidence = max(pipe.predict_proba([text])[0]) * 100
        else:
            output = int(svm.predict(cv.transform([text]))[0])  # 🛡️ Forcefully int
            confidence = max(svm.predict_proba(cv.transform([text]))[0]) * 100

        db.session.add(EmailHistory(user_id=current_user.id, email_text=text, prediction=output, confidence=round(confidence, 2)))
        db.session.commit()
        return render_template("show.html", prediction=output, confidence=round(confidence, 2))

    return render_template("index.html")

@app.route("/history")
@login_required
def history():
    records = EmailHistory.query.filter_by(user_id=current_user.id).all()
    return render_template("history.html", history=records)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            session.permanent = True
            return redirect(url_for("classify"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        if not is_secure_password(password):
            flash("Password must be at least 8 characters long and include a capital letter, a number, and a special character.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("register"))

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)