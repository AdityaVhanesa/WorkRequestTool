from flask import render_template
from flask_bcrypt import Bcrypt
from WRT.models import roles as Roles
from WRT import app

bcrypt = Bcrypt(app)


@app.route("/")
def Test():
    # ST.startWatchDog()
    allRoles = Roles.Role.get()
    print(allRoles)
    return render_template("login/user_login.html", roles = allRoles)


@app.route("/fail")
def Fail():
    return render_template("test/test_fail.html")
