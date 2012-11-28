from Athena.database import db
import md5


# the user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        md = md5.md5(unicode(password))
        self.password = md.hexdigest()

    def check_password(self, password):
        md = md5.md5(unicode(password))
        if self.password == md.hexdigest():
            return True
        else:
            return False

    def change_password(self, new_password):
        md = md5.md5(unicode(new_password))
        self.password = md.hexdigest()
        db.session.merge(self)
        db.session.commit()

    def add_friend(self, user):
        if not RelationShip.query.filter_by(from_user=self.id,
                                            to_user=user.id).all():
            relationship = RelationShip(from_user=self, to_user=user)
            db.session.add(relationship)
            db.session.commit()

    def add_friend_by_id(self, user_id):
        user = User.query.get(user_id)
        if user is not None:
            relationship = RelationShip(from_user=self, to_user=user)
            db.session.add(relationship)
            db.session.commit()

    def get_friends(self):
        friend_relation_list = RelationShip.query.filter_by(from_user=self.id)
        result = [_id.to_user for _id in friend_relation_list.all()]
        return result

    def __repr__(self):
        return "<User %s>" % self.username


class RelationShip(db.Model):
    """
    from_user follow to_user
    """
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, from_user, to_user):
        self.from_user = from_user.id
        self.to_user = to_user.id

    def __repr__(self):
        _from = User.query.get(self.from_user)
        _to = User.query.get(self.to_user)
        return "<RelationShip: %s follow %s>" % (_from.username,
                                                 _to.username)
