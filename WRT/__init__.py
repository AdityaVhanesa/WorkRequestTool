from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__, template_folder="templates")
encription = Bcrypt(app)
app.secret_key = "Secrate key for the Flask Work Request Tool"
