from flask import render_template, redirect, request, flash
from flask_bcrypt import Bcrypt

from WRT import app
from WRT.forms.loginForm import LoginForm
from WRT.forms.registraionForm import RegisterForm
from WRT.middlewares.authenticator import Authenticator
from WRT.models import managers as Managers
from WRT.models import roles as Roles
from WRT.models import users as Users

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect("/login")


@app.route("/login")
def login_page():
    return render_template("login/user_login.html", roles=Roles.Role.get())


@app.route("/logout")
def logout_user():
    Authenticator.clearSession()
    return redirect("/")


@app.route("/login/login_user", methods=['post'])
def login():
    form = LoginForm(request.form)
    if form.isValid():
        data = form.cleanData()
        userObject = Users.User.get(data, "email")

        if not userObject:
            flash("User not registerd", "login_email_error")
            return redirect("/")

        if Authenticator.Authenticate(data, userObject[0]):
            return redirect("/dashboard")
    return redirect("/")


@app.route("/register", methods=['post'])
def register_user():
    form = RegisterForm(request.form)
    if form.isValid():
        data = form.cleanData()
        userObject = Users.User.get(data, "email")
        print(userObject)
        if userObject:
            flash("User Already Exists", "login_error")
            return redirect("/")

        data["roles_id"] = Roles.Role.get({"role_name": request.form.get("role")}, "role_name")[0].id
        Users.User.save(data)
        if form.managerStatus:
            print("Saving Manager")
            Managers.Manager.save({"users_id": Users.User.get(data, "email")[0].id})
        flash("User Registerd", "login_error")
    return redirect("/")
