from werkzeug.security import generate_password_hash, check_password_hash

from . import db


users_permissions = db.Table('users_permissions',
                             db.Column('user_id', db.Integer(),
                                       db.ForeignKey('users.id')),
                             db.Column('permission_id', db.Integer(),
                                       db.ForeignKey('permissions.id')))


class User(db.Model):
    """
    The user model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())
    permissions = db.relationship('Permission', secondary=users_permissions,
                                  backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # add default permissions
        self.permissions = Permission.query.filter_by(default=True).all()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {"username": self.username}


class Permission(db.Model):
    """
    A permission is an action allowed for a user
    Typically, a permission is prefixed with a scope, usually the resource:
    Eg: posts_write, photos_create, users_delete
    """
    __tablename__ = 'permissions'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)

    @staticmethod
    def create_permissions():
        """
        Populates the permissions table with permission strings
        """
        perms = [("users_view_me", True),
                 ("users_view_all", False),
                 ("points_create", True)]
        for p in perms:
            perm = Permission.query.filter_by(name=p[0]).first()
            if perm is None:
                perm = Permission(name=p[0])
            perm.default = p[1]
            db.session.add(perm)
        db.session.commit()
