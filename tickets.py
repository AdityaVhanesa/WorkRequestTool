from flask import render_template,redirect,session,request, flash
from WorkRequestTool import app
from WorkRequestTool.models.ticket import Ticket
from WorkRequestTool.models.user import User


@app.route('/tickets/new')
def new_ticket():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('createTicket.html',user=User.get_by_id(data))


@app.route('/create/ticket',methods=['POST'])
def create_ticket():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Ticket.validate_ticket(request.form):
        return redirect('/tickets/new')
    data = {
        "department": request.form["department"],
        "ticketNumber": request.form["ticketNumber"],
        "ticket":   request.form["ticket"],
        "submittedBy": session["submittedBy"]
    }
    Ticket.save(data)
    return redirect('/dashboard')

@app.route('/tickets/<int:id>/edit')
def edit_ticket(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("editTicket.html",edit=Ticket.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/ticket',methods=['POST'])
def update_ticket():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "department": request.form["department"],
        "ticketNumber": request.form["ticketNumber"],
        "ticket": request.form["ticket"],
        "submittedBy": session["submittedBy"]
    }
    
    if not Ticket.validate_ticket(request.form):
        return redirect('/ticket/details/<int:id>')

@app.route('/tickets/<int:id>/respond')
def respond_ticket(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("respond.html",ticket=Ticket.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/response',methods=['POST'])
def update_response():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "startDate": request.form["startDate"],
        "completionDate": request.form["completionDate"],
        "reportLink": request.form["reportLink"],
        "comments": session["comments"]
    }
    
    if not Ticket.validate_ticket(request.form):
        return redirect('/tickets/' + data['id'] + '/repond')

    Ticket.update(data)
    return redirect('/dashboard')

@app.route('ticekt/details/<int:id>')
def show_ticket(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("ticketDetails.html",ticket=Ticket.get_one(data),user=User.get_by_id(user_data),users=User.get_all())

@app.route('/destroy/ticket/<int:id>')
def destroy_ticket(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Ticket.destroy(data)
    return redirect('/dashboard')

@app.route('/ticket/<int:id>/comment',methods=['POST'])
def add_comment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id,
        "comments": request.form["comments"]
    }
    Ticket.destroy(data)
    return redirect('/dashboard')