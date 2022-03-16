from minorcer_playerid_resetter import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Singapore')
singapore_now = datetime.now(tz)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="User")
    approval_status = db.Column(db.String(10), nullable=False, default="False")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}','{self.approval_status}')"


# admin = User(username="admin",email="admin@admin.com",password="987654321",role="Admin",approval_status="True")
# admin = User(username="ricky",email="ricky@admin.com",password="12345678",role="User",approval_status="True")

def current_time():
    tz = pytz.timezone('Asia/Singapore')
    return datetime.now(tz)


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playerid = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(10), nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"auditlogid: {self.id} -- Player ID: {self.playerid} -- UserID: {self.userid} -- Date: {self.datetime}"
