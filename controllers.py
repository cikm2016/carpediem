# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, make_response, g, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, or_

from app import app, db
from app.forms import ArticleForm,  JoinForm, LoginForm, AdminForm
from app.models import Article, Comment, User, Game, LoginLog, ChargeLog, ExchangeLog, Message, BlockIp, SportandNation, League, LeagueDetail, Game, BankAccount, UserBet, UserBetGame, LevelLimit, Ladder, LadderGame, AdjustDay ,Pincode

import re
import json
from datetime import date, datetime, timedelta
from time import strftime

from jinja2 import evalcontextfilter, Markup, escape
from urllib2 import urlopen

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

# convert newline to <br>
@app.template_filter('nl2br')
@evalcontextfilter
def nl2br(eval_ctx, value):
	result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
			for p in _paragraph_re.split(escape(value)))
	if eval_ctx.autoescape:
		result = Markup(result)
	return result
app.jinja_env.filters['nl2br'] = nl2br


#
# @index & article list
#



#############################################
############   signup, signin   #############
#############################################

@app.route('/', methods=['GET', 'POST'])
def main():
	if 'id' in session:
		return redirect(url_for('user_main'))
	else:
		if request.method == 'POST':
			account = request.form['account']
			password = request.form['password']
		
			try:
				user = User.query.filter(User.account == account).first()
			except Exception, e:
				print e

			if user is None:
				error = u'존재하지 않는 아이디입니다'
			elif user.password != password:
				error = u'비밀번호가 틀렸습니다.'
			else:
				#	관리자 일때
				if user.allow == 2:
					return redirect(url_for('main_admin'))

				elif user.allow == 0:
					#가입 대기중
					return render_template('main.html', error=u'가입승인 대기중인 아이디입니다.')
				else:
					if user.state == 1:
						return render_template('main.html', error=u'정지된 아이디입니다.')

					loginlog = LoginLog(
									ip = request.remote_addr,
									date = datetime.now()+timedelta(hours=9),
									user = user
									)
					db.session.add(loginlog)
					db.session.commit()
					
					session.permanent = True
					session['id'] = user.id
					session['nickname'] = user.nickname
					return redirect(url_for('user_main'))

			return render_template('main.html', error=error)
		return render_template('main.html')


# main for admin
@app.route('/admin', methods=['GET', 'POST'])
def main_admin():
	if 'admin' in session:
		return redirect(url_for('admin_main'))
	else:
		if request.method == 'POST':
			account = request.form['account']
			password = request.form['password']

			try:
				user = User.query.filter(User.account == account).first()
			except Exception, e:
				print e

			if user is None:
				pass
			#elif not check_password_hash(user.password, password):
			elif user.password != password:
				error = u'비밀번호가 틀렸습니다.'
			else:
				if user.allow != 2:
					return render_template('main_admin.html')
				else:
					session.permanent = True
					session['admin'] = user.id
					return redirect(url_for('admin_main'))

			return render_template('main_admin.html')
		return render_template('main_admin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		user = User.query.filter(User.account == request.form['account']).first()
		if user is None:
			nick = User.query.filter(User.nickname == request.form['nickname']).first()
			if nick is None:
				try:
					# 일단은 무조건 만들어냄.. 용규형이랑 이야기 필요
					pincode = Pincode.query.filter(Pincode.name == request.form['pincode']).first()
					if pincode is None:
						return render_template('signup.html', error=u'핀코드가 올바르지 않습니다')
					user = User(
							account = request.form['account'],
							password = request.form['password'],
							nickname = request.form['nickname'],
							phone = request.form['phone'],
							bank = request.form['bank'],
							bank_account = request.form['bank_account'],
							bank_name = request.form['bank_name'],
							bank_password = request.form['bank_password'],
							rec_person = request.form['rec_person'],
							ip = request.remote_addr,
							join_date = datetime.now()+timedelta(hours=9),
							pincode = pincode	
							)
					db.session.add(user)
					
					today = (datetime.now()+timedelta(hours=9)).date()
					try:
						adjust_today = AdjustDay.query.filter(AdjustDay.date == today).first()
					except Exception, e:
						print e
					if adjust_today is None:
						adjust_today = AdjustDay(
											date = (datetime.now()+timedelta(hours=9)).date()
											)
						db.session.add(adjust_today)
						db.session.commit()
											
					adjust_today.new_user += 1

					db.session.commit()
					return redirect(url_for('main'))
				except:
					return render_template('signup.html')
			else:
				return render_template('signup.html')
		else:
			return render_template('signup.html')

	else:
		return render_template('signup.html')


@app.route('/signout')
def signout():
	if 'id' in session:
		session.clear()
		return redirect(url_for('main'))
	elif 'admin' in session:
		session.clear()
		return redirect(url_for('main_admin'))
	else:
		return redirect(url_for('main'))

####################################
############   admin   #############
####################################

## 회원관리
## /admin/user/~~

# 로그인 후 메인 페이지
@app.route('/admin/main', methods=['GET'])
def admin_main():
	if 'admin' in session:
		return render_template('admin/adminmain.html')
	else:
		return redirect(url_for('main_admin'))

## 유저 관리 
## 가입 신청 회원 리스트
@app.route('/admin/user/wait', methods=['GET'])
def admin_user_wait():
	if 'admin' in session:
		userlist = User.query.filter(User.allow == 0).all()
		return render_template('admin/user_wait.html', userlist=userlist, menu='user')
	else:
		return redirect(url_for('admin_main'))


## 가입 신청 회원 수락 or 거절
@app.route('/admin/user/allow', methods=['POST'])
def admin_user_allow():
	if 'admin' in session:
		id = int(request.form['id'])
		allow = int(request.form['allow'])

		if allow == 1:
			user = User.query.get(id)
			if user is None:
				return jsonify(success=False)
			else:
				user.allow = 1
				db.session.commit()
				return jsonify(success=True)
		else:
			user = User.query.get(id)
			if user is None:
				return jsonify(success=False)
			else:
				db.session.delete(user)
				db.session.commit()
				return jsonify(success=True)
	else:
		return jsonify(success=False)

## 일반 회원 관리
@app.route('/admin/user/info', methods=['GET','POST'])
def admin_user_info():
	if 'admin' in session:
		if request.method == 'POST':
			type = int(request.form['searchtype'])
			level = int(request.form['searchlevel'])
			text = request.form['searchtext']	

			if level == 0:
				if type == 0:
					userlist = User.query.filter(User.allow == 1, User.account.contains(text)).all()
				elif type == 1:
					userlist = User.query.filter(User.allow == 1, User.nickname.contains(text)).all()
				elif type == 2:
					userlist = User.query.filter(User.allow == 1, User.ip.contains(text)).all()
				elif type == 3:
					userlist = User.query.filter(User.allow == 1, User.password.contains(text)).all()
				elif type == 4:
					userlist = User.query.filter(User.allow == 1, User.rec_person.contains(text)).all()
				else:
					userlist = User.query.filter(User.allow == 1).all()
			else:
				if type == 0:
					userlist = User.query.filter(User.level == level, User.allow == 1, User.account.contains(text)).all()
				elif type == 1:                                 
					userlist = User.query.filter(User.level == level, User.allow == 1, User.nickname.contains(text)).all()
				elif type == 2:                                 
					userlist = User.query.filter(User.level == level, User.allow == 1, User.ip.contains(text)).all()
				elif type == 3:
					userlist = User.query.filter(User.level == level, User.allow == 1, User.password.contains(text)).all()
				elif type == 4:
					userlist = User.query.filter(User.level == level, User.allow == 1, User.rec_person.contains(text)).all()
				else:                                           
					userlist = User.query.filter(User.level == level, User.allow == 1).all()
				

			return render_template('admin/user_info.html', userlist=userlist, menu='user')

		else:
			userlist = User.query.filter(User.allow == 1).all()
			return render_template('admin/user_info.html', userlist=userlist, menu='user')
			
	else:
		return redirect(url_for('admin_main'))

## 회원 접속 로그 확인
@app.route('/admin/user/loginlog/<int:id>', methods=['GET'])
def admin_user_loginlog(id):
	if 'admin' in session:
		user = User.query.get(id)
		if user is None:
			return render_template('404user.html')
		else:
			logs = user.loginlogs.order_by(desc(LoginLog.date)).all()

			return render_template('admin/user_loginlog.html',logs=logs, account=user.account)
	else:
		return redirect(url_for('admin_main'))

#회원 상세 정보 보기
@app.route('/admin/user/detail/<int:id>', methods=['GET'])
def admin_user_detail(id):
	if 'admin' in session:
		user = User.query.get(id)
		if user is None:
			return render_template('404user.html')
		else:
			log = user.loginlogs.order_by(desc(LoginLog.date)).first()
			leveldata = LevelLimit.query.filter(LevelLimit.level == user.level).first()
			return render_template('admin/user_detail.html',log=log, user=user, leveldata=leveldata)
	else:
		return redirect(url_for('admin_main'))


#회원 상세 정보 수정
@app.route('/admin/user/modify', methods=['POST'])
def admin_user_modify():
	if 'admin' in session:
		id = request.form['id']
		user = User.query.get(id)
		if user is None:
			return jsonify(success=False)
		else:
			user.bank = request.form['bank']
			user.bank_account = request.form['bank_account']
			user.bank_name = request.form['bank_name']
			user.level = int(request.form['level'])
			user.state = int(request.form['state'])
			user.danger = int(request.form['danger'])

			db.session.commit()

			return jsonify(success=True)
	else:
		return jsonify(success=False)

#회원 배팅 내역 보기
@app.route('/admin/user/view/bet/<int:id>', methods=['GET'])
def admin_user_view_bet(id):
	if 'admin' in session:
		user = User.query.get(id)

		if user is None:
			return render_template('404user.html')
		else:
			history = user.mybets.order_by(desc(UserBet.date)).all()
			#betlist = []

			#for h in history:
			#	betlist.append(h.betgames.all())

			return render_template('admin/user_bet.html', user=user,history=history)
	else:
		return redirect(url_for('admin_main'))


#회원 충전 내역보기
@app.route('/admin/user/view/charge/<int:id>', methods=['GET'])
def admin_user_view_charge(id):
	if 'admin' in session:
		user = User.query.get(id)

		if user is None:
			return render_template('404user.html')
		else:
			history = user.chargelogs.order_by(desc(ChargeLog.date)).all()

			return render_template('admin/user_charge.html', user=user,chargelist=history)
	else:
		return redirect(url_for('admin_main'))

#회원 충전 내역보기
@app.route('/admin/user/view/exchange/<int:id>', methods=['GET'])
def admin_user_view_exchange(id):
	if 'admin' in session:
		user = User.query.get(id)

		if user is None:
			return render_template('404user.html')
		else:
			history = user.exchangelogs.order_by(desc(ExchangeLog.date)).all()

			return render_template('admin/user_exchange.html', user=user,exchangelist=history)
	else:
		return redirect(url_for('admin_main'))

#회원 쪽지 보내기
@app.route('/admin/user/message/<int:id>', methods=['GET'])
def admin_user_message(id):
	if 'admin' in session:
		user = User.query.get(id)
		if user is None:
			return render_template('404user.html')
		else:
			return render_template('admin/user_message.html', id=user.id, nickname=user.nickname)
	else:
		return redirect(url_for('admin_main'))


#회원 쪽지 보내기
@app.route('/admin/user/send', methods=['POST'])
def admin_user_send():
	if 'admin' in session:
		id = int(request.form['id'])
		message = request.form['message']
		user = User.query.get(id)
		if user is None:
			return jsonify(success=False)
		else:
			msg = Message(
					message = message,
					user = user,
					date = datetime.now()+timedelta(hours=9)
					)
			db.session.add(msg)
			db.session.commit()
			return jsonify(success=True)
	else:
		return jsonify(success=False)
	

#회원 아이피 관리
@app.route('/admin/user/ip', methods=['GET', 'POST'])
def admin_user_ip():
	if 'admin' in session:
		if request.method == 'POST':
			ip = request.form['ip2']	
			iplist = BlockIp.query.filter(BlockIp.ip.contains(ip)).all()
			return render_template('admin/user_blockip.html', iplist=iplist, menu='user')

		else:
			iplist = BlockIp.query.all()
			return render_template('admin/user_blockip.html', iplist = iplist, menu='user')
	else:
		return redirect(url_for('main_admin'))


# 아이피 차단하기
@app.route('/admin/user/blockip', methods=['POST'])
def admin_user_blockip():
	if 'admin' in session:
		ip = request.form['ip']
		chk_ip = BlockIp.query.filter(BlockIp.ip == ip).first()
		if chk_ip is None:
			bip = BlockIp(
					ip = ip,
					date = datetime.now()+timedelta(hours=9)
					)
			db.session.add(bip)
			db.session.commit()
			return jsonify(success=True, ip=bip.ip, date=(bip.date).strftime("%Y-%m-%d %H:%M:%S"))
		else:
			return jsonify(success=False, msg=u'이미 차단된 아이피입니다.')

	else:
		return jsonify(success=False)


#차단 아이피 - 삭제
@app.route('/admin/user/ip/deleteall', methods=['POST'])
def admin_user_ip_deleteall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			ip = BlockIp.query.get(id)
			db.session.delete(ip)

		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 
		
#정지 회원 관리
@app.route('/admin/user/stop', methods=['GET'])
def admin_user_stop():
	if 'admin' in session:
		userlist = User.query.filter(User.state == 1).all()
		return render_template('admin/user_stop.html', userlist=userlist, menu='user')
	else:
		return redirect(url_for('main_admin'))

#관리자 회원 관리
@app.route('/admin/user/admin', methods=['GET'])
def admin_user_admin():
	if 'admin' in session:
		userlist = User.query.filter(User.allow == 2).all()
		return render_template('admin/user_admin.html', userlist=userlist, menu='user')
	else:
		return redirect(url_for('main_admin'))



## 리그관리
## /admin/league/~~

#종목 추가
@app.route('/admin/league/sport', methods=['GET', 'POST'])
def admin_league_sport():
	if 'admin' in session:
		if request.method == 'GET':
			sportlist = SportandNation.query.filter(SportandNation.type == 0).order_by(SportandNation.sort).all()
			return render_template('admin/league_sport.html', sportlist=sportlist, menu='league')
		else:
			sport = request.form['sport']
			san = SportandNation(
						type=0,
						name=sport
						)
			db.session.add(san)
			db.session.commit()
			
			return redirect(url_for('admin_league_sport'))
	else:
		return redirect(url_for('main_admin'))

#종목 수정 
@app.route('/admin/league/sport/modify', methods=['POST'])
def admin_league_sport_modify():
	if 'admin' in session:
		id = int(request.form['id'])
		name = request.form['name']
		sort = request.form['sort']

		sport = SportandNation.query.get(id)
		if sport is None:
			return jsonify(success=False)

		sport.name = name
		sport.sort = sort
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#종목 수정 - 선택 사항
@app.route('/admin/league/sport/allmodify', methods=['POST'])
def admin_league_sport_allmodify():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			name = d['name']
			sort = d['sort']

			sport = SportandNation.query.get(id)
			if sport is None:
				return jsonify(success=False)

			sport.name = name
			sport.sort = sort
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 
#종목 삭제
@app.route('/admin/league/sport/delete', methods=['POST'])
def admin_league_sport_delete():
	if 'admin' in session:
		id = int(request.form['id'])

		sport = SportandNation.query.get(id)
		if sport is None:
			return jsonify(success=False)

		db.session.delete(sport)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#국가 추가
@app.route('/admin/league/nation', methods=['GET', 'POST'])
def admin_league_nation():
	if 'admin' in session:
		if request.method == 'GET':
			nationlist = SportandNation.query.filter(SportandNation.type == 1).order_by(SportandNation.sort).all()
			return render_template('admin/league_nation.html', nationlist=nationlist, menu='league')
		else:
			nation = request.form['nation']
			san = SportandNation(
						type=1,
						name=nation
						)
			db.session.add(san)
			db.session.commit()
			
			return redirect(url_for('admin_league_nation'))
	else:
		return redirect(url_for('main_admin'))

#국가 수정 
@app.route('/admin/league/nation/modify', methods=['POST'])
def admin_league_nation_modify():
	if 'admin' in session:
		id = int(request.form['id'])
		name = request.form['name']
		sort = request.form['sort']

		sport = SportandNation.query.get(id)
		if sport is None:
			return jsonify(success=False)

		sport.name = name
		sport.sort = sort
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#국가 수정 - 선택 사항
@app.route('/admin/league/nation/allmodify', methods=['POST'])
def admin_league_nation_allmodify():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			name = d['name']
			sort = d['sort']

			sport = SportandNation.query.get(id)
			if sport is None:
				return jsonify(success=False)

			sport.name = name
			sport.sort = sort
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 
#국가 삭제
@app.route('/admin/league/nation/delete', methods=['POST'])
def admin_league_nation_delete():
	if 'admin' in session:
		id = int(request.form['id'])

		nation = SportandNation.query.get(id)
		if nation is None:
			return jsonify(success=False)

		db.session.delete(nation)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#국가 삭제
@app.route('/admin/league/nation/alldelete', methods=['POST'])
def admin_league_nation_alldelete():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])

			nation = SportandNation.query.get(id)
			if nation is None:
				return jsonify(success=False)

			db.session.delete(nation)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#리그 추가
@app.route('/admin/league/league', methods=['GET', 'POST'])
def admin_league_league():
	if 'admin' in session:
		if request.method == 'GET':
			nationlist = SportandNation.query.filter(SportandNation.type == 1).order_by(SportandNation.sort).all()
			sportlist = SportandNation.query.filter(SportandNation.type == 0).order_by(SportandNation.sort).all()

			leaguelist = League.query.order_by(League.sort).all()
			return render_template('admin/league_league.html', leaguelist=leaguelist, nationlist=nationlist, sportlist=sportlist, menu='league')
		else:
			check = request.form['check']
			if check == '1':
				nationlist = SportandNation.query.filter(SportandNation.type == 1).order_by(SportandNation.sort).all()
				sportlist = SportandNation.query.filter(SportandNation.type == 0).order_by(SportandNation.sort).all()

				sport = request.form['sport']
				nation = request.form['nation']
				name = request.form['league']

				leaguelist = League.query.filter(League.nation==nation, League.sport==sport, League.name.contains(name)).order_by(League.sort).all()
				return render_template('admin/league_league.html', leaguelist=leaguelist, nationlist=nationlist, sportlist=sportlist, menu='league')
			else:
				nation = request.form['nation']
				sport = request.form['sport']
				name = request.form['league']
				league = League(
							name = name,
							nation = nation,
							sport = sport
							)

				db.session.add(league)
				db.session.commit()
				
				return redirect(url_for('admin_league_league'))
	else:
		return redirect(url_for('main_admin'))

#리그명, 상태 수정
@app.route('/admin/league/league/modify', methods=['POST'])
def admin_league_league_modify():
	if 'admin' in session:
		id = int(request.form['id'])
		name = request.form['name']
		sort = request.form['sort']
		state = int(request.form['state'])

		league = League.query.get(id)
		if league is None:
			return jsonify(success=False)

		league.name = name
		league.sort = sort
		league.state = state
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#리그 수정 - 선택 사항
@app.route('/admin/league/league/allmodify', methods=['POST'])
def admin_league_league_allmodify():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			name = d['name']
			state = d['state']
			sort = d['sort']

			league = League.query.get(id)
			if league is None:
				return jsonify(success=False)

			league.name = name
			league.state = state
			league.sort = sort
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 
#리그 삭제
@app.route('/admin/league/league/delete', methods=['POST'])
def admin_league_league_delete():
	if 'admin' in session:
		id = int(request.form['id'])

		league = League.query.get(id)
		if league is None:
			return jsonify(success=False)

		db.session.delete(league)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

@app.route('/admin/league/league/alldelete', methods=['POST'])
def admin_league_league_alldelete():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = d['id']
			league = League.query.get(id)
			if league is None:
				return jsonify(success=False)

			db.session.delete(league)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#세부 리그 추가
@app.route('/admin/league/detail', methods=['GET', 'POST'])
def admin_league_detail():
	if 'admin' in session:
		if request.method == 'GET':
			leaguelist = League.query.filter(League.state==1).all()
			#detaillist = LeagueDetail.query.all()
			#return render_template('admin/league_detail.html', leaguelist=leaguelist,detaillist=detaillist, menu='league')
			return render_template('admin/league_detail.html', leaguelist=leaguelist, menu='league')
		else:
			leagueid = int(request.form['league'])
			name = request.form['name']
			home = request.form['home']
			away = request.form['away']
			menu = request.form['menu']
			game = request.form['game']

			league = League.query.get(leagueid)
			id = 0
			if league is not None:
				detail = LeagueDetail(
							name = name,
							home = home,
							away = away,
							menu = int(menu),
							game = int(game),
							league = league
							)
				db.session.add(detail)
				db.session.commit()
				id = detail.id
			
			return jsonify(success=True, id=id, name=name, home=home, away=away,menu=menu, game=game, league=league.name)
	else:
		return redirect(url_for('main_admin'))

#세부 리그 리스트
@app.route('/admin/league/detail/list', methods=['POST'])
def admin_league_detail_list():
	if 'admin' in session:
		# league id
		id = int(request.form['id'])

		league = League.query.get(id)
		detail = league.details.all()

		list = []
		for d in detail:
			tmp = {}
			tmp['id'] = d.id
			tmp['league'] = league.name
			tmp['name'] = d.name
			tmp['home'] = d.home
			tmp['away'] = d.away
			tmp['menu'] = d.menu
			tmp['game'] = d.game
			list.append(tmp)
		
		return jsonify(success=True, list=list)
	else:
		return jsonify(success=False) 

#세부 리그명, 상태 수정
@app.route('/admin/league/detail/modify', methods=['POST'])
def admin_league_detail_modify():
	if 'admin' in session:
		id = int(request.form['id'])
		name = request.form['name']
		home = request.form['home']
		away = request.form['away']
		menu = request.form['menu']
		game = request.form['game']

		detail = LeagueDetail.query.get(id)
		if detail is None:
			return jsonify(success=False)

		detail.name = name
		detail.home = home
		detail.away = away 
		detail.menu = menu
		detail.game = game
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 
#세부 리그명, 상태 수정
@app.route('/admin/league/detail/allmodify', methods=['POST'])
def admin_league_detail_allmodify():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			name = d['name']
			home = d['home']
			away = d['away']
			menu = d['menu']
			game = d['game']

			detail = LeagueDetail.query.get(id)
			if detail is None:
				return jsonify(success=False)

			detail.name = name
			detail.home = home
			detail.away = away 
			detail.menu = menu
			detail.game = game
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#세부 리그 삭제
@app.route('/admin/league/detail/delete', methods=['POST'])
def admin_league_detail_delete():
	if 'admin' in session:
		id = int(request.form['id'])

		league = LeagueDetail.query.get(id)
		if league is None:
			return jsonify(success=False)

		db.session.delete(league)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#세부 리그 삭제
@app.route('/admin/league/detail/alldelete', methods=['POST'])
def admin_league_detail_alldelete():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])

			league = LeagueDetail.query.get(id)
			if league is None:
				return jsonify(success=False)

			db.session.delete(league)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 


## 경기 등록/개시 
## /admin/register/~~

#경기 등록
@app.route('/admin/register/game', methods=['GET', 'POST'])
def admin_register_game():
	if 'admin' in session:
		if request.method == 'GET':
			leaguelist = League.query.all()
			gamelist = Game.query.filter(Game.state == 0, Game.finish == 0).all()

			return render_template('admin/register_game.html', leaguelist=leaguelist, gamelist=gamelist, menu='register')
		else:
			game = request.form['game']
			league_id = int(request.form['league'])
			date1 = request.form['date_first']
			date2 =  request.form['date_second']

			checked =  request.form.getlist('checked')

			for i in range(int(game)):
				for c in checked:
					detail = LeagueDetail.query.get(int(c))
					date = datetime.strptime(date1+' '+date2, '%Y-%m-%d %H:%M')

					game = Game(
							date= date,
							home= request.form['home_'+str(i)],
							away= request.form['away_'+str(i)],
							league_detail = detail
						)
					db.session.add(game)
			db.session.commit()
			
			return redirect(url_for('admin_register_game'))
	else:
		return redirect(url_for('main_admin'))

@app.route('/admin/register/game/getdetail', methods=['POST'])
def admin_register_game_getdetail():
	if 'admin' in session:
		id = int(request.form['id'])

		league = League.query.get(id)
		if league is None:
			return jsonify(success=False)

		detail = league.details.all()

		list = []
		for d in detail:
			tmp = {}
			tmp['id'] = d.id
			tmp['league'] = league.name
			tmp['name'] = d.name
			tmp['menu'] = d.menu
			list.append(tmp)

		db.session.commit()
		
		return jsonify(success=True, list=list)
	else:
		return jsonify(success=False) 
	

#등록 경기 수정
@app.route('/admin/register/game/modify', methods=['POST'])
def admin_register_game_modify():
	if 'admin' in session:
		id = int(request.form['id'])
		home_rate = request.form['home_rate']
		away_rate = request.form['away_rate']
		draw_rate = request.form['draw_rate']

		game = Game.query.get(id)
		if game is None:
			return jsonify(success=False)

		game.home_rate = home_rate
		game.away_rate = away_rate
		game.draw_rate = draw_rate
		db.session.commit()
		
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#등록 경기 - 선택된것 모두 수정
@app.route('/admin/register/game/applyall', methods=['POST'])
def admin_register_game_applyeall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			home = d['home']
			draw = d['draw']
			away = d['away']
			state = d['state']
			game = Game.query.get(id)

			game.home_rate = home
			game.away_rate = away

			if game.league_detail.menu == 2:
				game.handicap = draw
			else:
				game.draw_rate = draw
			game.state = state

		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#등록 경기 삭제
@app.route('/admin/register/game/delete', methods=['POST'])
def admin_register_game_delete():
	if 'admin' in session:
		id = int(request.form['id'])

		game = Game.query.get(id)
		betgames = game.betgames.count()
		if betgames >= 1:
			return jsonify(success=False, msg=u'이미 배팅된 경기입니다.')

		if game is None:
			return jsonify(success=False)

		db.session.delete(game)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#등록 경기 - 선택된것 모두 삭제
@app.route('/admin/register/game/deleteall', methods=['POST'])
def admin_register_game_deleteall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			game = Game.query.get(id)
			betgames = game.betgames.count()

			if betgames >= 1:
				return jsonify(success=False, msg=u'배팅된 경기가 있습니다.')

			db.session.delete(game)


		db.session.delete(game)
		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 


#등록 경기 - 승무패
@app.route('/admin/register/cross', methods=['GET', 'POST'])
def admin_register_cross():
	if 'admin' in session:
		if request.method == 'GET':
			list = Game.query.filter(Game.finish == 0).all()
			gamelist = []
			for game in list:
				if game.league_detail.menu == 1:
					gamelist.append(game)
					
			return render_template('admin/register_cross.html', gamelist=gamelist, menu='register')
		else:
			return redirect(url_for('admin_register_cross'))
	else:
		return redirect(url_for('main_admin'))


#등록 경기 - 승무패 상태 변경
@app.route('/admin/register/cross/apply', methods=['POST'])
def admin_register_cross_apply():
	if 'admin' in session:
		id = int(request.form['id'])
		state = int(request.form['state'])

		game = Game.query.get(id)
		if game is None:
			return jsonify(success=False)

		game.state = state
		db.session.commit()
		
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 


#등록 경기 - 승무패 상태 변경- 선택된것 모두
@app.route('/admin/register/cross/applyall', methods=['POST'])
def admin_register_cross_applyall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			game = Game.query.get(id)

			if game.league_detail.game == 1:
				game.draw_rate =  d['draw']
			elif game.league_detail.game == 2:
				game.handicap =  d['draw']
			else:
				game.standard =  d['draw']
				
			game.state =  d['state']
			game.home_rate =  d['home']
			game.away_rate =  d['away']

		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 


#등록 경기 - 핸디캡
@app.route('/admin/register/handicap', methods=['GET', 'POST'])
def admin_register_handicap():
	if 'admin' in session:
		if request.method == 'GET':
			list = Game.query.filter(Game.finish == 0).all()
			gamelist = []
			for game in list:
				if game.league_detail.menu == 2:
					gamelist.append(game)
					
			return render_template('admin/register_handicap.html', gamelist=gamelist, menu='register')
		else:
			return redirect(url_for('admin_register_handicap'))
	else:
		return redirect(url_for('main_admin'))
		
#등록 경기 - 핸디캡 배당, 상태 변경
@app.route('/admin/register/handicap/applyall', methods=['POST'])
def admin_register_handicap_applyall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			game = Game.query.get(id)

			game.state =  d['state']
			game.home_rate =  d['home']
			game.away_rate =  d['away']
			game.handicap =  d['handicap']

		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#등록 경기 - 스페셜
@app.route('/admin/register/special', methods=['GET', 'POST'])
def admin_register_special():
	if 'admin' in session:
		if request.method == 'GET':
			list = Game.query.filter(Game.finish == 0).all()
			gamelist = []
			for game in list:
				if game.league_detail.menu == 3:
					gamelist.append(game)
					
			return render_template('admin/register_special.html', gamelist=gamelist, menu='register')
		else:
			return redirect(url_for('admin_register_special'))
	else:
		return redirect(url_for('main_admin'))


#등록 경기 - 스페셜 배당 설정
@app.route('/admin/register/special/applyall', methods=['POST'])
def admin_register_special_applyall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			game = Game.query.get(id)

			game.state =  d['state']
			game.home_rate =  d['home']
			game.draw_rate =  d['draw']
			game.away_rate =  d['away']

		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#사다리 등록
@app.route('/admin/register/ladder', methods=['GET', 'POST'])
def admin_register_ladder():
	if 'admin' in session:
		if request.method == 'GET':
			ladderlist = Ladder.query.order_by(desc(Ladder.date)).all()

			return render_template('admin/register_ladder.html', ladderlist=ladderlist, menu='register')
		else:
			date = request.form['date']

			date = datetime.strptime(date, '%Y-%m-%d').date()

			test = Ladder.query.filter(Ladder.date == date).first()
			if test is not None:
				return redirect(url_for('admin_register_ladder'))
				
			ladder = Ladder(
					date = date
					)
			db.session.add(ladder)

			for i in range(1,289):
				game = LadderGame(
						number = i,
						ladder = ladder
						)
				db.session.add(game)


			db.session.commit()
			
			return redirect(url_for('admin_register_ladder'))
	else:
		return redirect(url_for('main_admin'))

#사다리 배당 입력
@app.route('/admin/register/ladder/applyall', methods=['POST'])
def admin_register_ladder_applyall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			ladder = Ladder.query.get(id)
			ladder.odd_rate =  d['odd']
			ladder.even_rate =  d['even']


		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#사다리 회차별 보기
@app.route('/admin/register/ladder/detail/<int:id>', methods=['GET'])
def admin_register_ladder_detail(id):
	if 'admin' in session:
		ladder = Ladder.query.get(id)
		date = ladder.date
		ladderlist = ladder.games.order_by(desc(LadderGame.number)).all()
		return render_template('admin/register_ladder_detail.html',date=date, ladderlist=ladderlist, menu='register')
	else:
		return redirect(url_for('main_admin'))

#사다리 회차별 결과 반영
@app.route('/admin/register/ladder/detail/applyall', methods=['POST'])
def admin_register_ladder_detail_applyall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			ladder = LadderGame.query.get(id)
			ladder.state =  d['state']

		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

## 경기 마감/복원 
## /admin/finish/~~

#경기 마감 - 승무패
@app.route('/admin/finish/cross', methods=['GET'])
def admin_finish_cross():
	if 'admin' in session:
		list = Game.query.filter(Game.finish == 0, Game.state ==3).all()
		gamelist = []
		for game in list:
			if game.league_detail.menu == 1:
				gamelist.append(game)

		return render_template('admin/finish_cross.html', gamelist=gamelist, menu='finish')
	else:
		return redirect(url_for('main_admin'))


#선택된 경기 마감  - 승무패
@app.route('/admin/finish/cross/all', methods=['POST'])
def admin_finish_cross_all():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			home_score = int(d['home_score'])
			away_score = int(d['away_score'])
			game = Game.query.get(id)

			if game is None:
				return jsonify(success=False)
			game.home_score = home_score
			game.away_score = away_score
			game.finish = 1
			
			if game.league_detail.game == 1:
				if home_score > away_score:
					game.win = 1
				elif home_score == away_score:
					game.win = 0
				else:
					game.win = -1
			elif game.league_detail.game == 2:
				if home_score + game.handicap > away_score:
					game.win = 1
				elif home_score + game.handicap == away_score:
					game.win = 0
				else:
					game.win = -1
			else:
				if home_score + away_score > game.standard:
					game.win = 1
				elif home_score + away_score == game.standard: 
					game.win = 0
				else:
					game.win = -1

			games = game.betgames.all()
			for g in games:	
				# 게임 결과 반영
				if game.win == 1:
					if g.betting == 1:
						g.isSuccess = 1
					else:
						userbet = UserBet.query.get(g.user_bet_id)
						userbet.state = -1

				elif game.win == 0:
					if g.betting == 0:
						g.isSuccess = 1
					else:
						userbet = UserBet.query.get(g.user_bet_id)
						userbet.state = -1

				else:
					if g.betting == -1:
						g.isSuccess = 1
					else:
						userbet = UserBet.query.get(g.user_bet_id)
						userbet.state = -1
			
			# 경기 결과 및 미당첨 배팅 업데이트
			db.session.commit()
						
			for g in games:	

				# 결과에 의해 유저들의 당첨여부 판단
				userbet = UserBet.query.get(g.user_bet_id)

				# 이미 당첨 실패 
				if userbet.state == -1:
					continue	
				# state:0 아직 당첨인지 모름, state=1 인 경우는 존재하지 않음
				elif userbet.state == 1:
					return jsonify(success=False)
				else:
					betlist = userbet.betgames.all()
					
					flag = 1
					for bet in betlist:
						if bet.isSuccess == 1:
							pass
						else:
							flag = 0	
							break

					#배팅 목록 모두 적중시 당첨
					#유저에게 당첨금 지급
					if flag == 1:
						userbet.state = 1
						user = User.query.get(userbet.user_id)
						user.money_crt += int((userbet.money_bet)*(userbet.rate))


		db.session.commit()
		return jsonify(success=True)
	else:
		return jsonify(success=False)

#경기 마감 리스트 - 핸디캡
@app.route('/admin/finish/handicap', methods=['GET'])
def admin_finish_handicap():
	if 'admin' in session:
		list = Game.query.filter(Game.finish == 0, Game.state ==3).all()
		gamelist = []
		for game in list:
			if game.league_detail.menu == 2:
				gamelist.append(game)
		return render_template('admin/finish_handicap.html', gamelist=gamelist, menu='finish')
	else:
		return redirect(url_for('main_admin'))

#선택된 경기 마감  -  핸디캡
@app.route('/admin/finish/handicap/all', methods=['POST'])
def admin_finish_handicap_all():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			home_score = int(d['home_score'])
			away_score = int(d['away_score'])
			game = Game.query.get(id)

			if game is None:
				return jsonify(success=False)
			game.home_score = home_score
			game.away_score = away_score
			game.finish = 1
			
			if (home_score + game.handicap) > away_score:
				game.win = 1
			elif (home_score + game.handicap) == away_score:
				game.win = 0
			else:
				game.win = -1

			games = game.betgames.all()
			for g in games:	
				# 게임 결과 반영
				if (home_score + game.handicap) > away_score:
					if g.betting == 1:
						g.isSuccess = 1
					else:
						userbet = UserBet.query.get(g.user_bet_id)
						userbet.state = -1

				elif (home_score + game.handicap) == away_score:
					if g.betting == 0:
						g.isSuccess = 1
					else:
						userbet = UserBet.query.get(g.user_bet_id)
						userbet.state = -1

				else:
					if g.betting == -1:
						g.isSuccess = 1
					else:
						userbet = UserBet.query.get(g.user_bet_id)
						userbet.state = -1
			
			# 경기 결과 및 미당첨 배팅 업데이트
			db.session.commit()
						
			for g in games:	

				# 결과에 의해 유저들의 당첨여부 판단
				userbet = UserBet.query.get(g.user_bet_id)

				# 이미 당첨 실패 
				if userbet.state == -1:
					continue	
				# state:0 아직 당첨인지 모름, state=1 인 경우는 존재하지 않음
				elif userbet.state == 1:
					return jsonify(success=False)
				else:
					betlist = userbet.betgames.all()
					
					flag = 1
					for bet in betlist:
						if bet.isSuccess == 1:
							pass
						else:
							flag = 0	
							break

					#배팅 목록 모두 적중시 당첨
					#유저에게 당첨금 지급
					if flag == 1:
						userbet.state = 1
						user = User.query.get(userbet.user_id)
						user.money_crt += int((userbet.money_bet)*(userbet.rate))


		db.session.commit()
		return jsonify(success=True)
	else:
		return jsonify(success=False)



#경기 마감 -  스페셜
@app.route('/admin/finish/special', methods=['GET'])
def admin_finish_special():
	if 'admin' in session:
		list = Game.query.filter(Game.finish == 0, Game.state ==3).all()
		gamelist = []
		for game in list:
			if game.league_detail.menu == 3:
				gamelist.append(game)
		return render_template('admin/finish_special.html', gamelist=gamelist, menu='finish')
	else:
		return redirect(url_for('main_admin'))

#사다리 마감 - 날짜별
@app.route('/admin/finish/ladder', methods=['GET', 'POST'])
def admin_finish_ladder():
	if 'admin' in session:
		ladderlist = Ladder.query.order_by(desc(Ladder.date)).all()

		return render_template('admin/finish_ladder.html', ladderlist=ladderlist, menu='finish')
		
	else:
		return redirect(url_for('main_admin'))

		
#사다리 마감 리스트 - 회차별
@app.route('/admin/finish/ladder/detail/<int:id>', methods=['GET'])
def admin_finish_ladder_detail(id):
	if 'admin' in session:
		ladder = Ladder.query.get(id)
		date = ladder.date

		ladderlist = ladder.games.filter(LadderGame.state==3).order_by(desc(LadderGame.number)).all()
		return render_template('admin/finish_ladder_detail.html', date=date, ladderlist=ladderlist, menu='finish')
	else:
		return redirect(url_for('main_admin'))


#사다리 회차별 마감
@app.route('/admin/finish/ladder/detail/applyall', methods=['POST'])
def admin_finish_ladder_detail_applyall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])
			ladder = LadderGame.query.get(id)
			ladder.win =  d['win']

			betlist = ladder.laddergames.all()
			for bet in betlist:
				userbet = UserBet.query.get(bet.user_bet_id)
				if int(bet.betting) == int(ladder.win):
					bet.isSuccess = 1
					userbet.state = 1
					
					user = User.query.get(userbet.user_id)
					user.money_crt += int((userbet.money_bet)*(userbet.rate))
						
				else:
					userbet.state = -1
					

		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 





#마감 경기 복원 
@app.route('/admin/finish/restore', methods=['GET', 'POST'])
def admin_finish_restore():
	if 'admin' in session:
		if request.method == 'GET':
			gamelist = Game.query.filter(Game.finish == 1).all()
			return render_template('admin/finish_restore.html', gamelist=gamelist, menu='finish')
		else:
			id = int(request.form['id'])
			game = Game.query.get(id)

			if game is None:
				return jsonify(success=False)
			game.finish = 0
			db.session.commit()
			return jsonify(success=True)
	else:
		return redirect(url_for('main_admin'))



## 입출금관리
## /admin/bank/~~

#충전신청 관리 
@app.route('/admin/bank/charge', methods=['GET'])
def admin_bank_charge():
	if 'admin' in session:
		chargelist = ChargeLog.query.filter(ChargeLog.charged == 0).order_by(desc(ChargeLog.date)).all()
		return render_template('admin/bank_charge.html', chargelist=chargelist, menu='bank')
	else:
		return redirect(url_for('main_admin'))

#충전신청 개별 수락
@app.route('/admin/bank/charge/allow', methods=['POST'])
def admin_bank_charge_allow():
	if 'admin' in session:
		id = int(request.form['id'])

		charge = ChargeLog.query.get(id)
		if charge is None:
			return jsonify(success=False)

		charge.charged = 1
		charge.date_finished = datetime.now()+timedelta(hours=9)
		charge.user.money_crt += charge.money
		charge.user.money_charge += charge.money

		today = (datetime.now()+timedelta(hours=9)).date()
		try:
			adjust_today = AdjustDay.query.filter(AdjustDay.date == today).first()
		except Exception, e:
			print e
		if adjust_today is None:
			adjust_today = AdjustDay(
								date = (datetime.now()+timedelta(hours=9)).date()
								)
			db.session.add(adjust_today)
			db.session.commit()
								
		adjust_today.charged += charge.money

		db.session.commit()
			
		#유저에게 쪽지?
		
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#충전신청 모두 수락
@app.route('/admin/bank/charge/allowall', methods=['POST'])
def admin_bank_charge_allowall():
	if 'admin' in session:
		data = json.loads(request.form['data'])

		today = (datetime.now()+timedelta(hours=9)).date()
		try:
			adjust_today = AdjustDay.query.filter(AdjustDay.date == today).first()
		except Exception, e:
			print e

		if adjust_today is None:
			adjust_today = AdjustDay(
								date = (datetime.now()+timedelta(hours=9)).date()
								)
			db.session.add(adjust_today)
			db.session.commit()
			
		for d in data:
			charge = ChargeLog.query.get(int(d['id']))
			if charge is None:
				return jsonify(success=False)

			charge.charged = 1
			charge.date_finished = datetime.now()+timedelta(hours=9)
			charge.user.money_crt += charge.money
			charge.user.money_charge += charge.money

			adjust_today.charged += charge.money

		db.session.commit()
			
		#유저에게 쪽지?
		
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 



#충전완료 내역 관리 
@app.route('/admin/bank/charge/complete', methods=['GET'])
def admin_bank_charge_complete():
	if 'admin' in session:
		chargelist = ChargeLog.query.filter(ChargeLog.charged == 1).order_by(desc(ChargeLog.date)).all()
		return render_template('admin/bank_charge_complete.html', chargelist=chargelist, menu='bank')
	else:
		return redirect(url_for('main_admin'))



#환전신청 관리 
@app.route('/admin/bank/exchange', methods=['GET'])
def admin_bank_exchange():
	if 'admin' in session:
		exchangelist = ExchangeLog.query.filter(ExchangeLog.exchanged == 0).order_by(desc(ExchangeLog.date)).all()
		return render_template('admin/bank_exchange.html', exchangelist=exchangelist, menu='bank')
	else:
		return redirect(url_for('main_admin'))

#환전신청 개별 수락
@app.route('/admin/bank/exchange/allow', methods=['POST'])
def admin_bank_exchange_allow():
	if 'admin' in session:
		id = int(request.form['id'])

		exchange = ExchangeLog.query.get(id)
		if exchange is None:
			return jsonify(success=False)

		exchange.exchanged = 1
		exchange.date_finished = datetime.now()+timedelta(hours=9)

		today = (datetime.now()+timedelta(hours=9)).date()
		try:
			adjust_today = AdjustDay.query.filter(AdjustDay.date == today).first()
		except Exception, e:
			print e

		if adjust_today is None:
			adjust_today = AdjustDay(
								date = (datetime.now()+timedelta(hours=9)).date()
								)
								
			db.session.add(adjust_today)
			db.session.commit()

		adjust_today.exchanged += exchange.money
		db.session.commit()
			
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#환전신청 모두 수락
@app.route('/admin/bank/exchange/allowall', methods=['POST'])
def admin_bank_exchange_allowall():
	if 'admin' in session:
		data = json.loads(request.form['data'])

		today = (datetime.now()+timedelta(hours=9)).date()
		try:
			adjust_today = AdjustDay.query.filter(AdjustDay.date == today).first()
		except Exception, e:
			print e

		if adjust_today is None:
			adjust_today = AdjustDay(
								date = (datetime.now()+timedelta(hours=9)).date()
								)
			db.session.add(adjust_today)
			db.session.commit()
								
		for d in data:
			exchange = ExchangeLog.query.get(int(d['id']))
			if exchange is None:
				return jsonify(success=False)

			exchange.exchanged = 1
			exchange.date_finished = datetime.now()+timedelta(hours=9)

			adjust_today.exchanged += exchange.money

		db.session.commit()
		
		return jsonify(success=True)
	else:
		return jsonify(success=False) 

#환전신청 개별 거절
@app.route('/admin/bank/exchange/deallow', methods=['POST'])
def admin_bank_exchange_deallow():
	if 'admin' in session:
		id = int(request.form['id'])

		exchange = ExchangeLog.query.get(id)
		if exchange is None:
			return jsonify(success=False)

		exchange.exchanged = -1
		exchange.date_finished = datetime.now()+timedelta(hours=9)
		exchange.user.money_crt += exchange.money

		db.session.commit()
			
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 


#환전신청 모두 거절 
@app.route('/admin/bank/exchange/deallowall', methods=['POST'])
def admin_bank_exchange_deallowall():
	if 'admin' in session:
		data = json.loads(request.form['data'])

		for d in data:
			exchange = ExchangeLog.query.get(int(d['id']))
			if exchange is None:
				return jsonify(success=False)

			exchange.exchanged = 1
			exchange.date_finished = datetime.now()+timedelta(hours=9)
			exchange.user.money_crt += exchange.money

		db.session.commit()
			
		#유저에게 쪽지?
		
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#환전완료 내역 관리 
@app.route('/admin/bank/exchange/complete', methods=['GET'])
def admin_bank_exchange_complete():
	if 'admin' in session:
		exchangelist = ExchangeLog.query.filter(ExchangeLog.exchanged != 0).order_by(desc(ExchangeLog.date)).all()
		return render_template('admin/bank_exchange_complete.html', exchangelist=exchangelist, menu='bank')
	else:
		return redirect(url_for('main_admin'))












#입금계좌 관리 - 레벨병 관리
@app.route('/admin/bank/account', methods=['GET'])
def admin_bank_account():
	if 'admin' in session:
		banklist = BankAccount.query.all()
		return render_template('admin/bank_account.html', banklist=banklist, menu='bank')
	else:
		return redirect(url_for('main_admin'))


#입금계좌 개별 수정
@app.route('/admin/bank/account/modify', methods=['POST'])
def admin_bank_account_modify():
	if 'admin' in session:
		id = int(request.form['id'])

		bank = request.form['bank']
		bank_account = request.form['bank_account']
		bank_name = request.form['bank_name']

		account = BankAccount.query.get(id)
		if account is None:
			return jsonify(success=False)

		account.bank = bank
		account.bank_account = bank_account
		account.bank_name = bank_name
		db.session.commit()

		
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 

#입금계좌 선택 동시 수정
@app.route('/admin/bank/account/modifyall', methods=['POST'])
def admin_bank_account_modifyall():
	if 'admin' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])

			bank = d['bank']
			bank_account = d['bank_account']
			bank_name = d['bank_name']

			account = BankAccount.query.get(id)
			if account is None:
				return jsonify(success=False)

			account.bank = bank
			account.bank_account = bank_account
			account.bank_name = bank_name
		db.session.commit()

		
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 


#정산 관리- 일 정산

@app.route('/admin/adjust/day', methods=['GET', 'POST'])
def admin_adjust_day():
	if 'admin' in session:
		if request.method == 'GET':
			targetday = (datetime.now()+timedelta(hours=9)).date()
			try:
				adjust_list = AdjustDay.query.filter(AdjustDay.date == targetday).all()
			except Exception, e:
				print e

			return render_template('admin/adjust_day.html',adjust_list=adjust_list, menu='adjust')
		else:
			start = request.form['date_start']
			end = request.form['date_end']

			date_start = datetime.strptime(start, '%Y-%m-%d')
			date_end = datetime.strptime(end, '%Y-%m-%d')

			try:
				adjust_list = AdjustDay.query.filter(AdjustDay.date >= date_start, AdjustDay.date <= date_end).order_by(desc(AdjustDay.date)).all()
			except Exception, e:
				print e

			return render_template('admin/adjust_day.html',adjust_list=adjust_list, menu='adjust')

	else:
		return redirect(url_for('main_admin'))


#지점 지사 페이지
@app.route('/admin/pincode', methods=['GET', 'POST'])
def admin_pincode():
	if 'admin' in session:
		if request.method == 'GET':
			list = Pincode.query.all()
			return render_template('admin/pincode.html', list=list, menu='pincode')
		else:
			pincode = Pincode(name=request.form['pincode'])
			db.session.add(pincode)
			db.session.commit()
			return redirect(url_for('admin_pincode'))
	else:
		return redirect(url_for('main_admin'))

#핀코드 별 유저 보기
@app.route('/admin/pincode/users/<int:id>', methods=['GET'])
def admin_pincode_users(id):
	if 'admin' in session:
		pin = Pincode.query.get(id)
		if pin is None:
			return render_template('404user.html')
		else:
			users = pin.users.all()
			return render_template('admin/pincode_users.html',pin=pin, users=users)
	else:
		return redirect(url_for('admin_main'))


#핀코드 변경
@app.route('/admin/pincode/modify', methods=['POST'])
def admin_pincode_modify():
	if 'admin' in session:
		id = request.form['id']	
		pincode = request.form['pincode']	

		pin = Pincode.query.get(id)
		if pin is None:
			return jsonify(success=False)

		pin.name = pincode
		db.session.commit()

		return jsonify(success=True, name=pincode)
	else:
		return jsonify(success=False)

#관리자 설정 페이지
@app.route('/admin/setting', methods=['GET', 'POST'])
def admin_setting():
	if 'admin' in session:
		if request.method == 'GET':
			list = LevelLimit.query.order_by(LevelLimit.level).all()
			return render_template('admin/setting.html', list=list, menu='setting')
		else:
			for i in range(7):
				leveldata = LevelLimit.query.filter(LevelLimit.level==(i+1)).first()
				
				leveldata.cross_minbet = request.form['cross_minbet_'+str(i+1)]
				leveldata.cross_maxbet = request.form['cross_maxbet_'+str(i+1)]
				leveldata.cross_maxgain = request.form['cross_maxgain_'+str(i+1)]
				
				leveldata.handicap_minbet = request.form['handicap_minbet_'+str(i+1)]
				leveldata.handicap_maxbet = request.form['handicap_maxbet_'+str(i+1)]
				leveldata.handicap_maxgain = request.form['handicap_maxgain_'+str(i+1)]

				leveldata.special_minbet = request.form['special_minbet_'+str(i+1)]
				leveldata.special_maxbet = request.form['special_maxbet_'+str(i+1)]
				leveldata.special_maxgain = request.form['special_maxgain_'+str(i+1)]

			db.session.commit()
			return redirect(url_for('admin_setting'))
	else:
		return redirect(url_for('main_admin'))

#관리자 설정 페이지- 네임드
@app.route('/admin/setting/named', methods=['GET', 'POST'])
def admin_setting_named():
	if 'admin' in session:
		if request.method == 'GET':
			list = LevelLimit.query.order_by(LevelLimit.level).all()
			return render_template('admin/setting_named.html', list=list, menu='setting')
		else:
			for i in range(7):
				leveldata = LevelLimit.query.filter(LevelLimit.level==(i+1)).first()
				
				leveldata.ladder_minbet = request.form['ladder_minbet_'+str(i+1)]
				leveldata.ladder_maxbet = request.form['ladder_maxbet_'+str(i+1)]
				leveldata.ladder_maxgain = request.form['ladder_maxgain_'+str(i+1)]
				
				leveldata.snail_minbet = request.form['snail_minbet_'+str(i+1)]
				leveldata.snail_maxbet = request.form['snail_maxbet_'+str(i+1)]
				leveldata.snail_maxgain = request.form['snail_maxgain_'+str(i+1)]

			db.session.commit()
			return redirect(url_for('admin_setting_named'))
	else:
		return redirect(url_for('main_admin'))
####################################
############   user    #############
####################################

## 유저 메인
@app.route('/user/main', methods=['GET'])
def user_main():
	if 'id' in session:
		return render_template('user/usermain.html')
	else:
		return redirect(url_for('main'))


## 승무패 메인
@app.route('/user/cross', methods=['GET'])
def user_cross():
	if 'id' in session:
		user = User.query.get(session['id'])
		level = LevelLimit.query.filter(LevelLimit.level == user.level).first()
		
		list = Game.query.filter(Game.finish == 0, Game.state == 1).order_by(desc(Game.date)).all()
		gamelist = []
		for game in list:
			if game.league_detail.menu == 1:
				gamelist.append(game)

		gamelist.sort(key=lambda x:x.league_detail, reverse=True)

		tmp = 0
		retlist = []
		tmplist = []
		for g in gamelist:
			if tmp != g.league_detail.id:
				tmp = g.league_detail.id
				tmplist = []
				retlist.append(tmplist)
				tmplist.append(g)
			else:
				tmplist.append(g)


		return render_template('user/cross.html',user=user, retlist=retlist, minbet=level.cross_minbet, maxbet=level.cross_maxbet, maxgain=level.cross_maxgain, menu='cross')
	else:
		return redirect(url_for('main'))

## 승무패 - 유저 배팅
@app.route('/user/cross/betting', methods=['POST'])
def user_cross_betting():
	if 'id' in session:
		user = User.query.get(session['id'])
		level = LevelLimit.query.filter(LevelLimit.level == user.level).first()

		data = json.loads(request.form['data'])
		money = int(request.form['money'])

		if level.cross_maxbet < money:
			return jsonify(success=False)
			
		rate = float(request.form['rate'])

		user_bet = UserBet(
						user = user,
						money_bet = money,
						rate = rate,
						game = 1, 
						date = datetime.now()+timedelta(hours=9)
					)

		today = (datetime.now()+timedelta(hours=9)).date()
		try:
			adjust_today = AdjustDay.query.filter(AdjustDay.date == today).first()
		except Exception, e:
			print e
		if adjust_today is None:
			adjust_today = AdjustDay(
								date = (datetime.now()+timedelta(hours=9)).date()
								)
			db.session.add(adjust_today)
			db.session.commit()
								
		adjust_today.bet_cnt += 1
		adjust_today.bet_money += money


		for d in data:
			game = Game.query.get(int(d['id']))
			try:
				bet = UserBetGame(
							game = game,
							user_bet = user_bet,
							betting = int(d['betting'])
						)
			except Exception, e:
				print e
				jsonify(success=False)

			db.session.add(bet)

		db.session.add(user_bet)

		user.bet_cnt += 1
		user.money_crt -= money
		
		db.session.commit()
		
		return jsonify(success=True)
	else:
		return jsonify(success=False)


## 핸디캡 메인
@app.route('/user/handicap', methods=['GET'])
def user_handicap():
	if 'id' in session:
		user = User.query.get(session['id'])
		level = LevelLimit.query.filter(LevelLimit.level == user.level).first()
		
		list = Game.query.filter(Game.finish == 0, Game.state == 1).order_by(desc(Game.date)).all()
		gamelist = []
		for game in list:
			if game.league_detail.menu == 2:
				gamelist.append(game)

		gamelist.sort(key=lambda x:x.league_detail, reverse=True)

		tmp = 0
		retlist = []
		tmplist = []
		for g in gamelist:
			if tmp != g.league_detail.id:
				tmp = g.league_detail.id
				tmplist = []
				retlist.append(tmplist)
				tmplist.append(g)
			else:
				tmplist.append(g)

		return render_template('user/handicap.html',user=user, retlist=retlist, minbet=level.handicap_minbet, maxbet=level.handicap_maxbet, maxgain=level.handicap_maxgain, menu='handicap')
	else:
		return redirect(url_for('main'))

## 핸디캡 - 유저 배팅
@app.route('/user/handicap/betting', methods=['POST'])
def user_handicap_betting():
	if 'id' in session:
		user = User.query.get(session['id'])
		level = LevelLimit.query.filter(LevelLimit.level == user.level).first()

		data = json.loads(request.form['data'])
		money = int(request.form['money'])

		if level.handicap_maxbet < money:
			return jsonify(success=False)
			
		rate = float(request.form['rate'])

		user_bet = UserBet(
						user = user,
						money_bet = money,
						rate = rate,
						game = 2, 
						date = datetime.now()+timedelta(hours=9)
					)

		today = (datetime.now()+timedelta(hours=9)).date()
		try:
			adjust_today = AdjustDay.query.filter(AdjustDay.date == today).first()
		except Exception, e:
			print e
		if adjust_today is None:
			adjust_today = AdjustDay(
								date = (datetime.now()+timedelta(hours=9)).date()
								)
			db.session.add(adjust_today)
			db.session.commit()
								
		adjust_today.bet_cnt += 1
		adjust_today.bet_money += money

		for d in data:
			game = Game.query.get(int(d['id']))
			try:
				bet = UserBetGame(
							game = game,
							user_bet = user_bet,
							betting = int(d['betting'])
						)
			except Exception, e:
				print e
				jsonify(success=False)

			db.session.add(bet)

		db.session.add(user_bet)

		user.bet_cnt += 1
		user.money_crt -= money
		
		db.session.commit()
		
		return jsonify(success=True)
	else:
		return jsonify(success=False)
		
## 스페셜 메인
@app.route('/user/special', methods=['GET'])
def user_special():
	if 'id' in session:
		user = User.query.get(session['id'])
		level = LevelLimit.query.filter(LevelLimit.level == user.level).first()
		
		list = Game.query.filter(Game.finish == 0, Game.state == 1).order_by(desc(Game.date)).all()
		gamelist = []
		for game in list:
			if game.league_detail.menu == 3:
				gamelist.append(game)

		gamelist.sort(key=lambda x:x.league_detail, reverse=True)

		tmp = 0
		retlist = []
		tmplist = []
		for g in gamelist:
			if tmp != g.league_detail.id:
				tmp = g.league_detail.id
				tmplist = []
				retlist.append(tmplist)
				tmplist.append(g)
			else:
				tmplist.append(g)

		return render_template('user/special.html', user=user, retlist=retlist, minbet=level.special_minbet, maxbet=level.special_maxbet, maxgain=level.special_maxgain, menu='special')
	else:
		return redirect(url_for('main'))

##스페셜 - 유저 배팅
@app.route('/user/special/betting', methods=['POST'])
def user_special_betting():
	if 'id' in session:
		user = User.query.get(session['id'])
		level = LevelLimit.query.filter(LevelLimit.level == user.level).first()

		data = json.loads(request.form['data'])
		money = int(request.form['money'])

		if level.special_maxbet < money:
			return jsonify(success=False)
			
		rate = float(request.form['rate'])

		user_bet = UserBet(
						user = user,
						money_bet = money,
						rate = rate,
						game = 3, 
						date = datetime.now()+timedelta(hours=9)
					)

		today = (datetime.now()+timedelta(hours=9)).date()
		try:
			adjust_today = AdjustDay.query.filter(AdjustDay.date == today).first()
		except Exception, e:
			print e
		if adjust_today is None:
			adjust_today = AdjustDay(
								date = (datetime.now()+timedelta(hours=9)).date()
								)
			db.session.add(adjust_today)
			db.session.commit()
								
		adjust_today.bet_cnt += 1
		adjust_today.bet_money += money

		for d in data:
			game = Game.query.get(int(d['id']))
			try:
				bet = UserBetGame(
							game = game,
							user_bet = user_bet,
							betting = int(d['betting'])
						)
			except Exception, e:
				print e
				jsonify(success=False)

			db.session.add(bet)

		db.session.add(user_bet)

		user.bet_cnt += 1
		user.money_crt -= money
		
		db.session.commit()
		
		return jsonify(success=True)
	else:
		return jsonify(success=False)

## 유저 배팅 내역 
@app.route('/user/betting/history', methods=['GET', 'POST'])
def user_betting_history():
	if 'id' in session:
		user = User.query.get(session['id'])
		history = user.mybets.order_by(desc(UserBet.date)).all()
		betlist = []

		for h in history:
			betlist.append(h.betgames.all())

		return render_template('user/betting_history.html',history=history,  betlist=betlist, menu='bet_history')

	else:
		return redirect(url_for('main'))


## 유저 배팅 내역 - 삭제
@app.route('/user/betting/history/delete', methods=['POST'])
def user_betting_history_delete():
	if 'id' in session:
		id = int(request.form['id'])
		user_bet = UserBet.query.get(id)
		
		if user_bet is None:
			return jsonify(success=False)

		db.session.delete(user_bet)
		db.session.commit()

		return jsonify(success=True)

	else:
		return jsonify(success=False)

## 유저 배팅 취소
@app.route('/user/betting/cancel', methods=['POST'])
def user_betting_cancel():
	if 'id' in session:
		id = int(request.form['id'])
		user_bet = UserBet.query.get(id)
		
		if user_bet is None:
			return jsonify(success=False)

		if (user_bet.date+timedelta(minutes=20)) < (datetime.now()+timedelta(hours=9)):
			return jsonify(success=False, msg=u'배팅후 20분이내에만 취소가 가능합니다.')
			
		for bet in user_bet.betgames:
			if bet.game.date < (datetime.now()+timedelta(hours=9)): 
				return jsonify(success=False, msg=u'경기 시작후엔 취소할수 없습니다.')
			
		
			
		user = User.query.get(session['id'])
		user.money_crt += user_bet.money_bet
		
		db.session.delete(user_bet)
		db.session.commit()

		return jsonify(success=True)

	else:
		return jsonify(success=False)


## 사다리
@app.route('/user/named/ladder', methods=['GET'])
def user_named_ladder():
	if 'id' in session:
		user = User.query.get(session['id'])
		level = LevelLimit.query.filter(LevelLimit.level == user.level).first()
		ladder = Ladder.query.filter(or_(Ladder.date==date.today(), Ladder.date==(date.today()+timedelta(days=1)))).all()

		ladderlist = []
		for lad in ladder:
			for game in lad.games.filter(or_(LadderGame.state==1,LadderGame.state==2)).order_by(desc(LadderGame.number)).all():
				ladderlist.append(game)



		return render_template('user/named_ladder.html', ladderlist=ladderlist, user=user, minbet=level.ladder_minbet, maxbet=level.ladder_maxbet, maxgain=level.ladder_maxgain, menu='ladder')

	else:
		return redirect(url_for('main'))

#사다리 배팅
@app.route('/user/named/ladder/betting', methods=['POST'])
def user_namd_ladder_betting():
	if 'id' in session:
		user = User.query.get(session['id'])
		level = LevelLimit.query.filter(LevelLimit.level == user.level).first()

		money = int(request.form['money'])

		if level.ladder_maxbet < money:
			return jsonify(success=False)
			
		rate = float(request.form['rate'])

		user_bet = UserBet(
						user = user,
						money_bet = money,
						rate = rate,
						game = 4,
						date = datetime.now()+timedelta(hours=9)
					)
		laddergame = LadderGame.query.get(int(request.form['id']))
		
		try:
			bet = UserBetGame(
						ladder_game = laddergame,
						user_bet = user_bet,
						betting = int(request.form['betting'])
					)
		except Exception, e:
			print e
			jsonify(success=False)

		db.session.add(bet)
		db.session.add(user_bet)
		

		user.bet_cnt += 1
		user.money_crt -= money
		
		db.session.commit()
		
		return jsonify(success=True)
	else:
		return jsonify(success=False)

## 경기결과
@app.route('/user/result', methods=['GET'])
def user_result():
	if 'id' in session:
		gamelist = Game.query.filter(Game.finish == 1).all()		

		tmp = 0
		retlist = []
		tmplist = []
		for g in gamelist:
			if tmp != g.league_detail.id:
				tmp = g.league_detail.id
				tmplist = []
				retlist.append(tmplist)
				tmplist.append(g)
			else:
				tmplist.append(g)
		return render_template('user/result.html', retlist=retlist, menu='result')
	else:
		return redirect(url_for('main'))







#############################################################
## 		유저 개인 관리
## 유저 캐쉬 충전
@app.route('/user/charge', methods=['GET', 'POST'])
def user_charge():
	if 'id' in session:
		if request.method == 'GET':
			user = User.query.get(session['id'])
			level = BankAccount.query.filter(BankAccount.level == user.level).first()
			return render_template('user/charge.html',user=user, level=level)
		else:
			user = User.query.get(session['id'])
			money = int(request.form['chargemoney'])

			charge = ChargeLog(
						user = user,
						money = money,
						date = datetime.now()+timedelta(hours=9)
						)

			db.session.add(charge)
			db.session.commit()
			return jsonify(success=True)
			
	else:
		return redirect(url_for('main'))

## 유저 충전 환전 내역
@app.route('/user/charge/history', methods=['GET', 'POST'])
def user_charge_history():
	if 'id' in session:
		user = User.query.get(session['id'])
		history = user.chargelogs.order_by(desc(ChargeLog.date)).all()

		return render_template('user/charge_history.html', history=history)

	else:
		return redirect(url_for('main'))

## 유저 충전 환전 내역
@app.route('/user/exchange/history', methods=['GET', 'POST'])
def user_exchange_history():
	if 'id' in session:
		user = User.query.get(session['id'])
		history_ex = user.exchangelogs.order_by(desc(ExchangeLog.date)).all()

		return render_template('user/exchange_history.html', history_ex=history_ex)

	else:
		return redirect(url_for('main'))

## 유저 캐쉬 환전
@app.route('/user/exchange', methods=['GET', 'POST'])
def user_exchange():
	if 'id' in session:
		if request.method == 'GET':
			user = User.query.get(session['id'])
			return render_template('user/exchange.html',user=user)
		else:
			user = User.query.get(session['id'])
			money = int(request.form['exchangemoney'])

			charge = ExchangeLog(
						user = user,
						money = money,
						date = datetime.now()+timedelta(hours=9)
						)

			db.session.add(charge)
			user.money_crt -= money

			db.session.commit()
			return jsonify(success=True)
			
	else:
		return redirect(url_for('main'))




## 내정보
@app.route('/user/mypage', methods=['GET'])
def user_mypage():
	if 'id' in session:
		user = User.query.get(session['id'])
		leveldata = LevelLimit.query.filter(LevelLimit.level == user.level).first()
		messages = user.messages.order_by(desc(Message.date)).all()
		return render_template('user/mypage.html',user=user, leveldata=leveldata, msgs = messages)
	else:
		return redirect(url_for('main'))


#내정보 수정
@app.route('/user/mypage/modify', methods=['POST'])
def user_mypage_modify():
	if 'id' in session:
		id = int(request.form['id'])
		user = User.query.get(id)
		if user is None:
			return jsonify(success=False)
		else:
			user.bank = request.form['bank']
			user.bank_account = request.form['bank_account']
			user.bank_name = request.form['bank_name']

			db.session.commit()

			return jsonify(success=True)
	else:
		return jsonify(success=False)


#내정보 - 쪽지 삭제
@app.route('/user/mypage/message/delete', methods=['POST'])
def user_mypage_message_delete():
	if 'id' in session:
		data = json.loads(request.form['data'])
		
		for d in data:
			id = int(d['id'])

			msg = Message.query.get(id)
			db.session.delete(msg)

		db.session.commit()
		return jsonify(success=True)
		
	else:
		return jsonify(success=False) 








##############################
#########  이벤트   ##########
##############################

@app.route('/event')
def event_list():
	if 'id' in session:
		context = {}

		context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()
		return render_template('event/list.html', context=context, menu='event')
	else:
		return redirect(url_for('main'))

##############################
#########  게시판   ##########
##############################

@app.route('/article')
def article_list():
	# html 파일에 전달할 데이터 Context
	if 'id' in session:
		context = {}

		context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()
		context['article_number'] = Article.query.count()
		return render_template('article/list.html', context=context, menu='article')
	else:
		return redirect(url_for('main'))

@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
	if 'id' in session:
		user = User.query.get(session['id'])
		if request.method == 'POST':
			title = request.form['title']
			content = request.form['content']

			if title != '' and content != '':
			#if form.validate_on_submit():
				article = Article(
						title=title,
						content=content,
						date_created=datetime.now()+timedelta(hours=9),
						user = user
						)
				# 데이터베이스에 데이터를 저장
				db.session.add(article)
				db.session.commit()

				return redirect(url_for('article_list'))
			return render_template('article/create.html', user=user, menu='article')
		else:
			return render_template('article/create.html', user=user, menu='article')
	else:
		return redirect(url_for('main'))

@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
	if 'id' in session:
		article = Article.query.get(id)

		# relationship을 활용한 query
		comments = article.comments.order_by(Comment.date_created).all()
		article.nofc += 1
		db.session.commit()

		return render_template('article/detail.html', article=article, comments=comments, menu='article')
	else:
		return redirect(url_for('main'))

@app.route('/article/like')
def article_like():
	id = int(request.args.get('id'))
	article = Article.query.get(id)
	article.like += 1

	db.session.commit()

	return jsonify(like=article.like)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
	if 'id' in session:
		article = Article.query.get(id)
		if session['id'] == article.user_id:

			if request.method == 'POST':
				title = request.form['title']
				content = request.form['content']

				if title != '' and content != '':
					article.title = title
					article.content = content

					db.session.commit()
					return redirect(url_for('article_detail', id=id))

			return render_template('article/update.html', menu='article', article=article)
		else:
			return redirect(url_for('article_detail', article=article))

	else:
		return redirect(url_for('main'))


@app.route('/article/delete', methods=['POST'])
def article_delete():
	if 'id' in session:
		id = int(request.form['id'])
		article = Article.query.get(id)
		if article.user_id == session['id']:

			db.session.delete(article)
			db.session.commit()

			return jsonify(success=True)
		else:	
			return jsonify(success=False)
			
	else:
		return jsonify(success=False)


@app.route('/article/search', methods=['GET'])
def article_search():
	if 'id' in session:	
		search = request.args.get('search')	
		context = {}
		context['article_list'] = Article.query.filter(Article.title.contains(search)).order_by(desc(Article.date_created)).all()

		return render_template('article/list.html', context=context, menu='article')
	else:
		return redirect(url_for('main'))




#
# @comment controllers
#
@app.route('/comment/create', methods=['POST'])
def comment_create():
	if 'id' in session:
	#비번 해쉬로 해야할듯
		user = User.query.get(session['id'])
		id = request.form['id']
		arc = Article.query.get(id)
		comment = Comment(
				user=user,
				content=request.form['comment'],
				article=arc,
				date_created=datetime.now()+timedelta(hours=9)
				)
		db.session.add(comment)
		db.session.commit()

		return redirect(url_for('article_detail', id=id))
	else:
		return redirect(url_for('main'))

@app.route('/comment/like/<int:id>', methods=['GET'])
def comment_like(id):
	comment = Comment.query.get(id)
	comment.like += 1

	db.session.commit()

	return redirect(url_for('article_detail', id=comment.article_id))

@app.route('/comment/delete', methods=['GET', 'POST'])
def comment_delete():
	if request.method == 'POST':
		comment_id = request.form['id']

		comment = Comment.query.get(comment_id)
		arc = Article.query.get(request.form['aid'])


		## hash 처리 나중에 해야할듯
		if request.form['passwd'] == comment.password:
			arc.nofc -= 1
			db.session.delete(comment)
			db.session.commit()

			return jsonify(success=True)
		return jsonify(success=False)
	return redirect(url_for('article_list'))



@app.before_request
def before_request():
	if 'id' in session:
		g.id = session['id']
		g.nick = session['nickname']
	if 'admin' in session:
		g.admin = session['admin']
#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
	print e
	return render_template('404.html'), 404
	
# Handle 405 errors
@app.errorhandler(405)
def method_not_found(e):
	print e
	return render_template('405.html'), 405

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
	print e
	return render_template('500.html'), 500
