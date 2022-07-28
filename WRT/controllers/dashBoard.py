from flask import render_template, session

from WRT import app
from WRT.middlewares.authenticator import loginRequired
from WRT.models import tickets as Tickets


@app.route("/dashboard")
@loginRequired
def dashBoard():
    if session.get("isManager"):
        ticketObjects = Tickets.Ticket.get({"status": 0}, "status")
    else:
        ticketObjects = Tickets.Ticket.get({
            "status": 0,
            "assigned_to": int(session.get("user_id"))
        }, "status", "assigned_to")
    if not ticketObjects:
        ticketObjects = []
    return render_template("dashBoard/dashBoard.html", tickets=ticketObjects)
