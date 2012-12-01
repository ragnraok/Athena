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
    chat_room_id = db.Column(db.Integer, db.ForeignKey("chat_room.id"),
                          nullable=False)
    record = db.Column(db.Text, nullable=False)

    def __init__(self, record, chat_room_id):
        self.chat_room_id = chat_room_id
        self.record = record

    def __repr__(self):
        return "<ChatRoomRecord \'%s\' for room %s>" % (self.record, self.chat_room)
