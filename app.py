from WRT import app
from WRT.controllers import users, dashBoard, tickets

if __name__ == '__main__':
    app.run(debug=True, port=8080)