import datetime

from Athena.database import db
from Athena.user.models import User


class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, unique=True)
    launcher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    records = db.relationship('ChatRoomRecord', backref='chat_room',
                              lazy='dynamic')

    def __init__(self, title, launcher_id):
        self.title = title
        self.launcher_id = launcher_id

    def __repr__(self):
        user = User.query.get(self.launcher_id)
        return "<ChatRoom %s, launcher is %s>" % (self.title, user.username)


class ChatRoomRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    chat_room_id = db.Column(db.Integer, db.ForeignKey("chat_room.id"),
                          nullable=False)
    record = db.Column(db.Text, nullable=False)
    send_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, sender_id, chat_room_id, record, send_time=None):
        self.sender_id = sender_id
        self.chat_room_id = chat_room_id
        self.record = record
        if send_time is None:
            send_time = datetime.datetime.now()
        self.send_time = send_time

    def __repr__(self):
        return "<ChatRoomRecord \'%s\' for room %s>" % (self.record, self.chat_room)
