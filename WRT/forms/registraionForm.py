import re
from flask_bcrypt import Bcrypt
from WRT import encription
from flask import flash


class RegisterForm:
    def __init__(self, post):
        self.first_name = post.get("first_name")
        self.last_name = post.get("last_name")
        self.email = post.get("email")
        self.password = post.get("password")
        self.confirm_password = post.get("confirm-password")
        self.managerStatus = post.get("manager_status")

        self.__emailRegEx = re.compile(r"^\S+@\S+\.\S+$")

    def __str__(self):
        return f"{self.first_name} | {self.last_name} | {self.email}"

    def isValid(self):
        validFlag = True
        validFlag = self.validateFirst_name() and validFlag
        validFlag = self.validateLast_name() and validFlag
        validFlag = self.validateEmail() and validFlag
        validFlag = self.validatePassword() and validFlag
        return validFlag

    def validateFirst_name(self):
        if self.first_name:
            if len(self.first_name) >= 2:
                return True

            flash("Must be more than 2 characters", "first_name_error")
            return False

        flash("Missing", "first_name_error")
        return False

    def validateLast_name(self):
        if self.last_name:
            if len(self.last_name) >= 2:
                return True
            flash("Must be more than 2 characters", "last_name_error")
            return False

        flash("Missing", "last_name_error")
        return False

    def validateEmail(self):
        if self.email:
            if self.__emailRegEx.match(self.email):
                return True
            flash("Invalid Email", "email_error")
            return False

        flash("Missing", "email_error")
        return False

    def validatePassword(self):
        if self.password:
            if len(self.password) >= 8:
                if self.confirm_password:
                    if self.password == self.confirm_password:
                        return True

                    flash("Password does not match", "confirm_password_error")
                    return False

                flash("Missing", "confirm_password_error")
                return False

            flash("Password must be 8 characters long", "password_error")
            return False

        flash("Missing", "password_error")
        return False

    def cleanData(self):
        if self.isValid():
            self.first_name = self.first_name.lower()
            self.last_name = self.last_name.lower()
            self.password = encription.generate_password_hash(self.password)
            self.managerStatus = True if self.managerStatus == "True" else False

        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }