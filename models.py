# -*-coding:utf-8-*-
"""
models.py
"""
from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	account = db.Column(db.String(255))
	password = db.Column(db.String(255))
	phone = db.Column(db.String(255))
	bank_account = db.Column(db.String(255))
	bank = db.Column(db.String(255))
	money = db.Column(db.Integer, default=0)

	rec_person = db.Column(db.String(255))
	allow = db.Column(db.Integer, default=0)
	join_date = db.Column(db.DateTime())

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	sport = db.Column(db.Integer)
	league = db.Column(db.String(255))
	home = db.Column(db.String(255))
	home_rate = db.Column(db.Float, default=0.0)
	away = db.Column(db.String(255))
	away_rate = db.Column(db.Float, default=0.0)
	draw_rate = db.Column(db.Float, default=0.0)
	state = db.Column(db.Integer, default=0)
	score = db.Column(db.String(255))
	result = db.Column(db.Integer, default=0)	
	date = db.Column(db.DateTime())

#Talk Room
class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	like = db.Column(db.Integer, default=0)
	nick = db.Column(db.String(255))
	password = db.Column(db.String(255))
	content = db.Column(db.Text())
	nofc = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime())


#Comment of TalkRoom
class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	like = db.Column(db.Integer, default=0)
	article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
	article = db.relationship('Article',
			backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))

	nick = db.Column(db.String(255))
	password = db.Column(db.String(255))
	content = db.Column(db.Text())
	date_created = db.Column(db.DateTime())


