# -*-coding:utf-8-*-
from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	account = db.Column(db.String(255))
	password = db.Column(db.String(255))
	nickname = db.Column(db.String(255))
	phone = db.Column(db.String(255))
	bank = db.Column(db.String(255))
	bank_account = db.Column(db.String(255))
	bank_name = db.Column(db.String(255))
	ip = db.Column(db.String(255))
	rec_person = db.Column(db.String(255))

	state = db.Column(db.Integer, default=0)
	danger = db.Column(db.Integer, default=2)
	level = db.Column(db.Integer, default=1)
	
	#총 배팅수
	bet_cnt = db.Column(db.Integer, default=0)
	#현재 보유 금액
	money_crt = db.Column(db.Integer, default=0)
	#충전 총량
	money_charge = db.Column(db.Integer, default=0)
	#기본 배팅금
	money_bet = db.Column(db.Integer, default=0)
	# 1:allow, 0:wait 2:admin
	allow = db.Column(db.Integer, default=0)

	join_date = db.Column(db.DateTime())


#############################################
####    로그인, 충전, 환전 로그데이터    ####
#############################################

## user login log
class LoginLog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(255))
	date = db.Column(db.DateTime())

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User',backref=db.backref('loginlogs', cascade='all, delete-orphan', lazy='dynamic'))
	

## charge log
class ChargeLog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	money = db.Column(db.Integer)

	date = db.Column(db.DateTime())
	date_finished = db.Column(db.DateTime())

	charged = db.Column(db.Integer, default=0)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User',backref=db.backref('chargelogs', cascade='all, delete-orphan', lazy='dynamic'))

## exchange log
class ExchangeLog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	money = db.Column(db.Integer)

	date = db.Column(db.DateTime())
	date_finished = db.Column(db.DateTime())

	exchanged = db.Column(db.Integer, default=0)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User',backref=db.backref('exchangelogs', cascade='all, delete-orphan', lazy='dynamic'))


#message to user
class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	check = db.Column(db.Integer, default=0)
	message = db.Column(db.String(255))
	date = db.Column(db.DateTime())

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User',backref=db.backref('messages', cascade='all, delete-orphan', lazy='dynamic'))

class BlockIp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(255))
	date = db.Column(db.DateTime())
	




#############################################
#### 국가, 종목, 리그, 세부리그 메타정보 ####
#############################################

class SportandNation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#0: sport, 1: nation
	type = db.Column(db.Integer)
	name = db.Column(db.String(255))
	
class League(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	nation = db.Column(db.String(255)) 
	sport = db.Column(db.String(255)) 
	# 0: end, 1: on
	state = db.Column(db.Integer, default=1)

class LeagueDetail(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	home = db.Column(db.String(255)) 
	away = db.Column(db.String(255)) 
	menu = db.Column(db.String(255))
	game = db.Column(db.String(255))

	league_id = db.Column(db.Integer, db.ForeignKey('league.id'))
	league = db.relationship('League',
			backref=db.backref('details', cascade='all, delete-orphan', lazy='dynamic'))

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	home = db.Column(db.String(255))
	home_rate = db.Column(db.Float, default=0.0)
	away = db.Column(db.String(255))
	away_rate = db.Column(db.Float, default=0.0)
	draw_rate = db.Column(db.Float, default=0.0)

	#0:등록, 1:개시, 2:중지, 3:종료
	state = db.Column(db.Integer, default=0)
	finish = db.Column(db.Integer, default=0)

	home_score = db.Column(db.Integer, default=0)
	away_score = db.Column(db.Integer, default=0)

	win = db.Column(db.Integer) 

	date = db.Column(db.DateTime())

	league_detail_id = db.Column(db.Integer, db.ForeignKey('league_detail.id'))
	league_detail = db.relationship('LeagueDetail',
			backref=db.backref('games', cascade='all, delete-orphan', lazy='dynamic'))

# 레벨별 입금계좌 테이블
class BankAccount(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	level = db.Column(db.Integer)
	bank = db.Column(db.String(255))
	bank_account = db.Column(db.String(255))
	bank_name = db.Column(db.String(255))


# 레벨별 제한금액 테이블
class LevelLimit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	level = db.Column(db.Integer)

	cross_minbet = db.Column(db.Integer)
	cross_maxbet = db.Column(db.Integer)
	cross_maxgain = db.Column(db.Integer)

	handicap_minbet = db.Column(db.Integer)
	handicap_maxbet = db.Column(db.Integer)
	handicap_maxgain = db.Column(db.Integer)

	special_minbet = db.Column(db.Integer)
	special_maxbet = db.Column(db.Integer)
	special_maxgain = db.Column(db.Integer)
#############################################
####  유저 배팅 정보, 배팅한 게임 정보   ####
#############################################

class UserBet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('mybets', cascade='all, delete-orphan', lazy='dynamic'))

	money_bet = db.Column(db.Integer)
	rate = db.Column(db.Float)

	state = db.Column(db.Integer, default=0)
	date = db.Column(db.DateTime())



class UserBetGame(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	game = db.relationship('Game', backref=db.backref('betgames', cascade='all, delete-orphan', lazy='dynamic'))

	user_bet_id = db.Column(db.Integer, db.ForeignKey('user_bet.id'))
	user_bet = db.relationship('UserBet', backref=db.backref('betgames', cascade='all, delete-orphan', lazy='dynamic'))

	#1: home, 0: draw, -1: away
	betting = db.Column(db.Integer)

	isSuccess = db.Column(db.Integer, default=0)


#############################################
####               게시판                ####
#############################################
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


