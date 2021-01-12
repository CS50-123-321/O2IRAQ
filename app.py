from flask import Flask, flash, jsonify, redirect, render_template, request, session
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import sqlite3
from flask import url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from my import login_required
from flask_fontawesome import FontAwesome
#hello m
import os
import datetime as dt
#he
app = Flask(__name__)
# my database
db = SQL("sqlite:///identifier.sqlite")
fa = FontAwesome(app)
# Configure session to use filesystem (instead of signed cookies)
# session config
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route("/", methods=["GET", "POST"])
def getin():
    """Homepage"""
    session.clear()
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return "must provide username"
        if not password:
            return "must provide password"
        check = db.execute("select * from register where user_name = :username", username=username)
        password_decrption = check_password_hash(check[0]["password"], request.form.get("password"))
        if not check or password_decrption == False:
            return "You don't have an count!"
        session["user_id"] = check[0]["user_id"]
        # abubkr

        return redirect("/home")
    else:
        return render_template("login.html")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """Homepage"""
    """Current_user = db.execute("select user_name from register where user_id = :user_id", user_id=session["user_id"])
    current_user = current_user[0]["user_name"]
    current_user = current_user.split()[0]
    current_user = current_user.capitalize()"""
    posts = db.execute("select * from user_activity where user_id != 0")
    posts.reverse()
    noti_posts = db.execute("select * from user_activity where user_id != 0 and user_id != :user_id ORDER BY post DESC LIMIT 30",user_id=session["user_id"])
    noti_posts.reverse()
    #return render_template("home.html", noti_posts = noti_posts)
    return render_template("home.html", posts=posts, noti_posts=noti_posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("registeration.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        confirmation = request.form.get("confirmation")
        sex = request.form.get("sex")
        city = request.form.get("city")
        print("------->",username, password, email, confirmation, sex, city)
        #birthday = request.form.get("birthday")
        #job = request.form.get("job")
        # consider update your database tobe not null.
        # if not username or not password or not sex or not email or not city or not birthday or not job:
        """if not username or not password or not sex or not email or not city:
            return "Make sure to fill the required information!"""
        if password != confirmation:
            return "pass != conform", 403
        insertion = db.execute(
            "insert into register (user_name, password, email, sex, city) values (:username,:password, :email, :sex,:city)",
            username=username, password=generate_password_hash(password), email=email, sex=sex, city=city)

        session["user_id"] = insertion
        return redirect("/home")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return "must provide username"
        if not password:
            return "must provide password"

        check = db.execute("select * from register where user_name = :username", username=username)
        password_decrption = check_password_hash(check[0]["password"], request.form.get("password"))
        if not check or password_decrption == False:
            return "You don't have an count!"
        session["user_id"] = check[0]["user_id"]
        # abubkr

        return redirect("/home")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_info = db.execute("select * from register where user_id = :user_id", user_id=session["user_id"])
    user_name = user_info[0]['user_name']
    user_name = user_name.capitalize()
    user_city = user_info[0]['city']
    user_sex = user_info[0]["sex"]
    user_email = user_info[0]["email"]
    user_job = user_info[0]["job"]
    user_bd = user_info[0]['birthday']
    posts = db.execute("select * from user_activity where user_id = :user_id", user_id=session["user_id"])
    posts.reverse()
    print(posts)
    """counter_insert = db.execute("SELECT max(post_counter) FROM numbers where user_id = :user_id",
                                user_id=session["user_id"])"""

    #return render_template("profile.html", user_name=user_name, user_city=user_city, user_bd=user_bd, posts=posts,counter_insert=counter_insert[0]["max(post_counter)"])
    return render_template("profile.html", user_name=user_name, user_city=user_city, user_bd=user_bd, posts=posts,user_sex= user_sex, user_email=user_email, user_job=user_job)

@app.route("/activity", methods=["GET", "POST"])
@login_required
def activity():
    if request.method == "GET":
        return render_template("activity.html")
    else:
        content = request.form.get("text_area")
        print("------------",content)

        name = db.execute("select user_name from register where user_id = :user_id", user_id=session["user_id"])
        name = name[0]["user_name"]
        content_insert = db.execute("insert into user_activity (post, user_name, user_id, date)values (:content,:name,:user_id, current_timestamp)",
            content=content, name=name, user_id=session["user_id"])
        # consider using forign key
        post_counter = db.execute("SELECT COUNT(post) FROM user_activity WHERE user_id=:user_id",
                                  user_id=session["user_id"])
        counter_update = db.execute("UPDATE numbers SET post_counter = :post_counter where user_id = :user_id",
                                    post_counter=post_counter[0]["COUNT(post)"], user_id=session["user_id"])
        if not counter_update:
               counter_insert = db.execute("insert into numbers (post_counter,user_id) values (:post_counter, :user_id)",
                                    post_counter=post_counter[0]["COUNT(post)"], user_id=session["user_id"])
        return redirect("/home")

@app.route("/upload", methods=["GET", "POST"])
def convert_pic():
    if request.method == "POST":
        image = request.files["image"]
        with open(image, "rb") as file:
            image = file.read()
        pic_insert = db.execute("insert into register(profile_pic) values (:image)", image=image)
    else:

        return render_template('tst.html')

@app.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    user_name = request.form.get("search")
    #user_name = "ABUBKR"
    all_names_dic = db.execute("select user_name from user_activity")
    result_list1 = []
    result_list2 = []
    print(user_name)
    for name in range(len(all_names_dic)):
        all_names = all_names_dic[name]["user_name"]
        if len(all_names.split()) > 1:
            fname_splited = str(all_names.split()[0])
            if fname_splited == user_name:

                if all_names not in result_list1:
                    result_list1.append(all_names)
        elif len(all_names.split()) == 1:
            if all_names == user_name:
                if all_names not in result_list2:
                    result_list2.append(all_names)
    return render_template("lookup.html", lookup_item1=result_list1, lookup_item2=result_list2)




@app.route("/user_profile", methods=["GET", "POST"])
@login_required
def user_profile():
    return render_template("profile.html")

@app.route("/notification", methods=["GET", "POST"])
@login_required
def notification():
    current_user = db.execute("select user_name from register where user_id = :user_id", user_id=session["user_id"])
    current_user = current_user[0]["user_name"]
    current_user = current_user.split()[0]
    current_user = current_user.capitalize()
    posts = db.execute("select * from user_activity where user_id != 0 and user_id != :user_id ORDER BY post DESC LIMIT 30",user_id=session["user_id"])
    posts.reverse()
    #return render_template("Ins R
    return render_template("noti.html", posts=posts, current_user=current_user)