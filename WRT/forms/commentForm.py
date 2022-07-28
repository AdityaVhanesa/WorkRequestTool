from flask import flash


class CommentForm:
    def __init__(self, post):
        self.comment = post.get("comment")

    def __str__(self):
        return f"{self.comment}"

    def isValid(self):
        validFlag = True
        validFlag = self.validateComment() and validFlag
        return validFlag

    def validateComment(self):
        if self.comment:
            return True
        flash("Missing", "comment_box_error")
        return False

    def cleanData(self):
        return {
            "comment": self.comment
        }
