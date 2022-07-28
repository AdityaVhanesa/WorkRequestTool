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
            "assigned_to": int(session.get("user_id")),
        }, "status", "assigned_to")

        ticketObjects_2 = Tickets.Ticket.get({
            "status": 0,
            "raised_by": int(session.get("user_id")),
        }, "status", "raised_by")
        if not ticketObjects:
            ticketObjects = []
        if not ticketObjects_2:
            ticketObjects_2 = []
        ticketObjects += ticketObjects_2
    if not ticketObjects:
        ticketObjects = []
    return render_template("dashBoard/dashBoard.html", tickets=ticketObjects)
