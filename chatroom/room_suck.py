from gevent.event import Event
from gevent import monkey
monkey.patch_all()
from Athena.chatroom.models import ChatRoomRecord
from Athena.database import db


class RoomSuck(object):
    """
    store the online room users and events
    """
    def __init__(self):
        self.room_users = {}
        self.room_events = {}

    @classmethod
    def create_instance(cls):
        if hasattr(cls, "__instance"):
            return cls.__instance
        else:
            cls.__instance = cls()
            return cls.__instance

    def join_room(self, room_id, user_id):
        if room_id not in self.room_users:
            self.room_users[room_id] = []
        if user_id not in self.room_users[room_id]:
            self.room_users[room_id].append(user_id)

        if room_id not in self.room_events:
            self.room_events[room_id] = Event()

    def exit_room(self, room_id, user_id):
        if room_id not in self.room_users:
            return
        if user_id not in self.room_users[room_id]:
            return
        self.room_users[room_id].remove(user_id)
        if len(self.room_users[room_id]) == 0:
            del self.room_users[room_id]
            del self.room_events[room_id]

    def is_in_room(self, room_id, user_id):
        if room_id not in self.room_users:
            return False
        if user_id not in self.room_users[room_id]:
            return False
        return True

    def send_message(self, sender_id, room_id, message):
        record = ChatRoomRecord(sender_id, room_id, message)
        db.session.add(record)
        db.session.commit()

        if room_id in self.room_events:
            self.room_events[room_id].set()
            self.room_events[room_id].clear()

    def update_message(self, room_id):
        if room_id in self.room_events:
            print 'update'
            self.room_events[room_id].wait()

    def get_room_online_user_num(self, room_id):
        if room_id not in self.room_users:
            return 0
        return len(self.room_users[room_id])

    def get_room_online_users(self, room_id):
        if room_id not in self.room_users:
            return None
        return self.room_users[room_id]

    def exit_all_room(self, user_id):
        """
        use in logout
        """
        for room in self.room_users:
            if user_id in room:
                room.remove(user_id)

room_manager = RoomSuck.create_instance()
