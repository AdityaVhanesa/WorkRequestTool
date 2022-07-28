from datetime import datetime

from flask import render_template, request, session, redirect
from WRT.middlewares.emailBackEnd import EmailBackend
from WRT import app
from WRT.forms.commentForm import CommentForm
from WRT.forms.newTicketForm import TicketForm
from WRT.models import comments as Comments
from WRT.models import departments as Departments
from WRT.models import reports as Reports
from WRT.models import tickets as Tickets
from WRT.models import users as Users


@app.route('/ticket/new')
def new_ticket():
    return render_template('tickets/createTicket.html', departments=Departments.Department.get())


@app.route("/ticket/create", methods=["post"])
def create_ticket():
    form = TicketForm(request.form)
    if form.isValid():
        data = form.cleanData()
        departmentObject = Departments.Department.get({"name": request.form.get("department")}, "name")[0]
        data["functional_group"] = departmentObject.id
        data["raised_by"] = int(session.get("user_id"))
        Tickets.Ticket.save(data)
        ticketObject = Tickets.Ticket.getLatest()[0]
        userObject = Users.User.get({"id": int(session.get("user_id"))}, "id")[0]
        commentObject = None
        data = {
            "ticketObject": ticketObject,
            "userObject": userObject,
            "commentObject": commentObject,
            "notification_type": "N"
        }
        email = EmailBackend(data)
        email.main()
        return redirect("/dashboard")
    return redirect("/ticket/new")


@app.route('/ticket/<int:id>/edit')
def edit_ticket(id):
    ticketObject = Tickets.Ticket.get({"id": id}, "id")[0]
    departments = Departments.Department.get()
    return render_template("tickets/edit.html", ticket=ticketObject, departments=departments)


@app.route('/ticket/<int:id>/details')
def ticket_details(id):
    ticketObject = Tickets.Ticket.get({"id": id}, "id")[0]
    comments = Comments.Comment.get({"posted_on": id}, "posted_on")
    if not comments:
        comments = []
    return render_template("tickets/details.html", ticket=ticketObject, comments=comments)


@app.route("/ticket/<int:id>/assign")
def ticket_assign(id):
    userObject = Users.User.get({"id": session.get("user_id")}, "id")[0]
    userObject = Users.User.get({"roles_id": userObject.role.id}, "roles_id")
    return render_template("tickets/assign.html", users=userObject, ticket_id=id)


@app.route("/ticket/<int:id>/assign_user", methods=["post"])
def assign_user(id):
    data = {"assigned_to": int(request.form.get("assigned")),
            "id": id}

    Tickets.Ticket.update(data, values=["assigned_to"], location=["id"])
    ticketObject = Tickets.Ticket.get(data, "id")[0]
    userObject = Users.User.get({"id": int(request.form.get("assigned"))}, "id")[0]
    commentObject = None
    data = {
        "ticketObject": ticketObject,
        "userObject": userObject,
        "commentObject": commentObject,
        "notification_type": "A"
    }
    email = EmailBackend(data)
    email.main()
    return redirect("/dashboard")


@app.route('/ticket/<int:id>/response')
def ticket_response(id):
    return render_template("tickets/response.html", ticket_id = id)


@app.route('/ticket/<int:id>/update', methods=["post"])
def update_ticket(id):
    form = TicketForm(request.form)
    if form.isValid():
        data = form.cleanData()
        departmentObject = Departments.Department.get({"name": request.form.get("department")}, "name")[0]
        data["functional_group"] = departmentObject.id
        data["raised_by"] = int(session.get("user_id"))
        data["id"] = id
        Tickets.Ticket.update(data)
        return redirect("/dashboard")
    return redirect(f"/ticket/{id}/edit")


@app.route("/ticket/<int:id>/close")
def close_ticket(id):
    Tickets.Ticket.update({"status": 1, "id": id}, values=["status"], location=["id"])
    return redirect("/dashboard")


@app.route("/ticket/<int:id>/response/record", methods=["post"])
def ticket_response_update(id):
    start_date = request.form.get("startDate")
    close_date = request.form.get("completionDate")
    report_link = request.form.get("reportLink")
    comment = request.form.get("comments")
    if report_link == "":
        flash("Missing", "report_link_error")
        return redirect(f"/ticket/{id}/reponse")
    if start_date == "":
        start_date = datetime.now()
    if close_date == "":
        close_date = datetime.now()

    data = {
        "id": id,
        "closed_at": close_date,
        "report_id": id,
        "start_at": start_date,
        "comment": comment,
        "report_link": report_link
    }
    Reports.Report.save(data)
    report_id = Reports.Report.get({"report_link": report_link}, "report_link")[0].id
    data["report_id"] = report_id
    Tickets.Ticket.update(data, values=["closed_at", "report_id", "start_at"], location=["id"])

    if comment != "":
        data["posted_on"] = id
        data["posted_by"] = int(session.get("user_id"))
        Comments.Comment.save(data)

    return redirect(f"/ticket/{id}/details")


# @app.route('/tickets/<int:id>/respond')
# def respond_ticket(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id": id
#     }
#     user_data = {
#         "id": session['user_id']
#     }
#     return render_template("respond.html", ticket=Ticket.get_one(data), user=User.get_by_id(user_data))
#
#
# @app.route('/update/response', methods=['POST'])
# def update_ticket():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "startDate": request.form["startDate"],
#         "completionDate": request.form["completionDate"],
#         "reportLink": request.form["reportLink"],
#         "comments": session["comments"]
#     }
#
#     if not Ticket.validate_ticket(request.form):
#         return redirect('/tickets/' + data['id'] + '/repond')
#
#     Ticket.update(data)
#     return redirect('/index')
#
#
# @app.route('/details/<int:id>')
# def show_ticket(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id": id
#     }
#     user_data = {
#         "id": session['user_id']
#     }
#     return render_template("show_ticket.html", ticket=Ticket.get_one(data), user=User.get_by_id(user_data),
#                            users=User.get_all())
#
#
# @app.route('/destroy/ticket/<int:id>')
# def destroy_ticket(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id": id
#     }
#     Ticket.destroy(data)
#     return redirect('/index')
#
#
@app.route('/ticket/<int:id>/comment', methods=['POST'])
def add_comment(id):
    form = CommentForm(request.form)
    if form.isValid():
        data = form.cleanData()
        data["posted_on"] = id
        data["posted_by"] = int(session.get("user_id"))
        Comments.Comment.save(data)
        commentObject = Comments.Comment.getLatest()[0]
        userObject = Users.User.get({"id": int(session.get("user_id"))}, "id")[0]
        ticketObject = Tickets.Ticket.get({"id": id}, "id")[0]
        data = {
            "ticketObject": ticketObject,
            "userObject": userObject,
            "commentObject": commentObject,
            "notification_type": "C"
        }
        email = EmailBackend(data)
        email.main()
    return redirect(f"/ticket/{id}/details")
