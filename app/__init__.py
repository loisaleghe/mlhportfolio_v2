import os
from flask import Flask, render_template, send_from_directory, json, request
from dotenv import load_dotenv

# from . import db
from werkzeug.security import check_password_hash, generate_password_hash

# from app.db import get_db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


load_dotenv()
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
# db.init_app(app)


class UserModel(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


@app.route("/")
def home():
    return render_template("index.html", title="MLH DRAGON BLOG", url=os.getenv("URL"))


@app.route("/home")
def index():
    return render_template("index.html", title="MLH DRAGON BLOG", url=os.getenv("URL"))


# so we don't have to always go through environment variables
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


@app.route("/blogs")
def blog_page():
    dir = os.path.realpath(os.path.dirname(__file__))
    json_dir = os.path.join(dir, "static/data", "blogs.json")
    data = json.load(open(json_dir))
    return render_template("blogs.html", blogs=data["blogs"])


@app.route("/showblog")
def showblog():
    id = int(request.args.get("id"))

    dir = os.path.realpath(os.path.dirname(__file__))
    json_dir = os.path.join(dir, "static/data", "blogs.json")
    data = json.load(open(json_dir))
    blogs = data

    blog = blogs["blogs"][id]
    print(blog)
    return
    # return render_template('showblog.html', blog=blog)


@app.route("/projects")
def project_page():
    return render_template("project.html")


@app.route("/health", methods=["GET"])
def health_status():
    return "200 status ok"


@app.route("/team")
def team_page():
    return render_template("team.html", title="Team Dragon's Den")


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(request)
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return f"User {username} created successfully"
        else:
            return error, 418

    # TODO: Return a restister page
    # return "Register Page not yet implemented", 501
    return render_template("register.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            return "Login Successful", 200
        else:
            return error, 418

    # TODO: Return a login page
    # return "Login Page not yet implemented", 501
    return render_template("login.html")
