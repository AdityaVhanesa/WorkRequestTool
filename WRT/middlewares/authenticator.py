import threading
import time

from flask import session, flash, redirect

from WRT import encription
from WRT.models import managers as Managers


def loginRequired(function):
    def innerFunction(*args, **kwargs):
        if not Authenticator.isAthenticated and Authenticator.isSessionExpired:
            return redirect("/")
        return function(*args, **kwargs)

    return innerFunction


class Authenticator:
    isAthenticated = False
    timeOutPeriod = 600
    isSessionExpired = False

    def __init__(self):
        pass

    @classmethod
    def Authenticate(cls, data, userObject):
        cls.clearSession()
        if encription.check_password_hash(userObject.password, data['password']):
            session["user_id"] = userObject.id
            managerObject = Managers.Manager.get({"users_id": userObject.id}, "users_id")
            if managerObject:
                session["isManager"] = True
            cls.isAthenticated = True
            cls.isSessionExpired = False
            cls.startWatchDog()
            return True
        flash("Incorrect Password", "login_password_error")
        return False

    @classmethod
    def clearSession(cls):

        session.clear()
        cls.isAthenticated = False
        cls.isSessionExpired = True

    @classmethod
    def task_countPeriod(cls):
        time.sleep(cls.timeOutPeriod)
        cls.isSessionExpired = True
        cls.isAthenticated = False

    @classmethod
    def startWatchDog(cls):
        threading.Thread(target=cls.task_countPeriod).start()
