from flask import flash


class TicketForm:
    def __init__(self, post):
        self.title = post.get("title")
        self.ticket = post.get("ticket")

    def __str__(self):
        return f"{self.title}"

    def isValid(self):
        validFlag = True
        validFlag = self.validateTitle() and validFlag
        validFlag = self.validateTicket() and validFlag
        return validFlag

    def validateTitle(self):
        if self.title:
            return True

        flash("Missing", "ticket_title_error")
        return False

    def validateTicket(self):
        if self.ticket:
            return True
        flash("Missing", "ticket_ticket_error")
        return False

    def cleanData(self):

        return {
            "title": self.title,
            "description": self.ticket
        }
