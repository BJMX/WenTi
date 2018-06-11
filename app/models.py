# coding:utf8
import pymysql
import app.config as config
from flask import Flask
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)
    addtime = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username

    def check_pwd(self, pwd):
        return check_password_hash(self.password, pwd)


class Question(db.Model):
    __tablename__ = 'Question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    title = Column(String(500), nullable=False)
    label = Column(Integer, nullable=False)
    detail = Column(Text, nullable=True)
    addtime = Column(DateTime, nullable=False)

    authorq = db.relationship('User', backref=db.backref('questions'))

    def __repr__(self):
        return "<Title %r>" % self.title


class Spark(db.Model):
    __tablename__ = 'Spark'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    text = Column(Text, nullable=False)
    addtime = Column(DateTime, nullable=False)

    author = db.relationship('User', backref=db.backref('sparks'))

    def __repr__(self):
        return "<id %d>" % self.id


class Comment(db.Model):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    comment = Column(Text, nullable=False)
    addtime = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey('Question.id'), nullable=False)

    author = db.relationship('User', backref=db.backref('comments'))
    question = db.relationship('Question', backref=db.backref('comments'))

    def __repr__(self):
        return "<id %d>" % self.id


if __name__ == '__main__':
    db.create_all()
