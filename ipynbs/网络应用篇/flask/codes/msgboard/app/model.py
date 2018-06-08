

#导入ORM模块
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')

    def __repr__(self):
        return '''<Role: {id} name: {name}>'''.format(id = self.id,
                                  name = self.name)

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    message = db.relationship('Message', backref='user')

    #密码的写法:
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)


    def __repr__(self):
        return '''<User: {id}
        name: {name}
        role_id: {role_id}
        email: {email}>'''.format(id = self.id,
                                  name = self.name,
                                 role_id = self.role_id,
                                 email = self.email)
    def is_correct_password(self, plaintext):
        if bcrypt.check_password_hash(self._password, plaintext):
            return True

        return False

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<message: {id} - {time} - {content}>'.format(id = self.id,
                                                             time=self.timestamp,
                                                             content = self.content)
