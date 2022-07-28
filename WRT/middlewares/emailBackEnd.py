from __future__ import print_function

import base64
import os.path
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class EmailBackend:

    def __init__(self, data):
        self.credentials = "WRT.json"
        self.sender = 'workrequesttool@gmail.com'
        self.service = None
        self.ticketObject = data["ticketObject"]
        self.userObject = data["userObject"]
        self.commentObject = data["commentObject"]
        self.notificationType = data["notification_type"]
        if self.notificationType == "C":
            self.to = self.ticketObject.assigned_to.email
        else:
            self.to = self.userObject.email

        self.credObject = None
        self.scopes = ['https://www.googleapis.com/auth/gmail.compose']

    def main(self):
        pass
        # if not self.credObject or not self.credObject.valid:
        #     if self.credObject and self.credObject.expired and self.credObject.refresh_token:
        #         self.credObject.refresh(Request())
        #     else:
        #         flow = InstalledAppFlow.from_client_secrets_file(
        #             self.credentials, self.scopes)
        #         self.credObject = flow.run_local_server(port=0)
        #     # Save the credentials for the next run
        #     with open('token.json', 'w') as token:
        #         token.write(self.credObject.to_json())
        #
        # try:
        #     # Call the Gmail API
        #     self.service = build('gmail', 'v1', credentials=self.credObject)
        #     message = self.create_notification()
        #     self.send_notification(message)
        #
        # except HttpError as error:
        #     print(f'An error occurred: {error}')

    def create_notification(self):
        message, subject = "NA"
        if self.notificationType == "N":
            message, subject = self._newTaskNotification()
        if self.notificationType == "A":
            message, subject = self._newTaskAssignmentNotificatiion()
        if self.notificationType == "C":
            message, subject = self._newCommentNotification()
        print(message)
        print(subject)
        message = MIMEText(message)
        message["From"] = self.sender
        message["To"] = self.to
        message["Subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
        return {
            'raw': raw_message.decode("utf-8")
        }

    def send_notification(self, message):
        try:
            message = self.service.users().messages().send(userId="me", body=message).execute()
            print('Message Id: %s' % message['id'])
            return message
        except Exception as e:
            print('An error occurred: %s' % e)
            return None

    def _newCommentNotification(self):
        return f'''
               NEW COMMENT ALERT 

               {self.userObject} is Commented on the follwoing ticket

               TICKET
               --------------------------------------------------------
               ID          :-> {self.ticketObject.id}
               TITLE       :-> {self.ticketObject.title}
               DESCRIPTION :-> {self.ticketObject.description}
               RAISED ON   :-> {self.ticketObject.created_at}
               RAISED BY   :-> {self.ticketObject.raised_by}
               --------------------------------------------------------

               Comment
               --------------------------------------------------------
               {self.commentObject.comment}
               --------------------------------------------------------
               
               
               Click HERE to reply or view more details


               Happy Ticketing :)


               Team,
               Ticket Organizer,
               Work Request Tool
               ''', f"{self.ticketObject.title} has new comment"

    def _newTaskAssignmentNotificatiion(self):
        return f'''
        NEW TASK ASSIGNMENT ALERT

        You have been assigned to the following ticket. 


        TICKET
        --------------------------------------------------------
        ID          :-> {self.ticketObject.id}
        TITLE       :-> {self.ticketObject.title}
        DESCRIPTION :-> {self.ticketObject.description}
        RAISED ON   :-> {self.ticketObject.created_at}
        RAISED BY   :-> {self.ticketObject.raised_by}
        --------------------------------------------------------

        Click HERE to start working or view more details


        Happy Ticketing :)


        Team,
        Ticket Organizer,
        Work Request Tool
        ''', f"{self.ticketObject.title} Has been assigned to you"

    def _newTaskNotification(self):
        return f'''
        NEW TASK ALERT
        
        {self.ticketObject.raised_by} is created new ticket for department.
        Please find more informations below, 
        
        
        TICKET
        --------------------------------------------------------
        ID          :-> {self.ticketObject.id}
        TITLE       :-> {self.ticketObject.title}
        DESCRIPTION :-> {self.ticketObject.description}
        RAISED ON   :-> {self.ticketObject.created_at}
        RAISED BY   :-> {self.ticketObject.raised_by}
        --------------------------------------------------------
        
        Click Here to assign ticket to your team...!
        
        
        Happy Ticketing :)
        
        
        Team,
        Ticket Organizer,
        Work Request Tool
        ''', f"{self.ticketObject.raised_by} has raised new Ticket"
