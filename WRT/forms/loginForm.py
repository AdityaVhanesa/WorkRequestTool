import re

from flask import flash


class LoginForm:
    def __init__(self, post):
        self.email = post.get("email")
        self.password = post.get("password")
        self.__emailRegEx = re.compile(r"^\S+@\S+\.\S+$")

    def __str__(self):
        return f"{self.email}"

    def isValid(self):
        validFlag = True
        validFlag = self.validateEmail() and validFlag
        validFlag = self.validatePassword() and validFlag
        return validFlag

    def validateEmail(self):
        if self.email:
            if self.__emailRegEx.match(self.email):
                return True

            flash("Not a valid email address", "login_email_error")
            return False

        flash("Missing", "login_email_error")
        return False

    def validatePassword(self):
        if self.password:
            if len(self.password) >= 8:
                return True
            flash("Must be more than 8 characters", "login_password_error")
            return False

        flash("Missing", "login_password_error")
        return False

    def cleanData(self):
        if self.isValid():
            self.email = self.email.lower()

        return {
            "email": self.email,
            "password": self.password
        }