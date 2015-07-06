# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, make_response, g, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

from app import app, db
from app.forms import ArticleForm, CommentForm, JoinForm, LoginForm, AdminForm
from app.models import Article, Comment, User, Game

import re
import json
from datetime import date, datetime, timedelta
from time import strftime

from jinja2 import evalcontextfilter, Markup, escape

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


# main for user
@app.route('/', methods=['GET', 'POST'])
def main():
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			account = form.account.data
			password = form.password.data

			user = User.query.filter(User.account == account).first()

			if user is None:
				form.account.errors.append(u'존재하지 않는 아이디입니다.')
			elif not check_password_hash(user.password, password):
				form.password.errors.append(u'비밀번호가 잘못되었습니다.')
			else:
				if user.allow == 0:
					flash(u'가입 승인 대기중', 'danger')
					return redirect(url_for('main'))
				session.permanent = True
				session['id'] = user.id
				return redirect(url_for('betting_normal'))

			return render_template('main.html', form=form)
		else:
			return render_template('main.html', form=form)
	return render_template('main.html', form=form)


# main for admin
@app.route('/admin', methods=['GET', 'POST'])
def main_admin():
	form = AdminForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			account = form.account.data
			password = form.password.data

			user = User.query.filter(User.account == account).first()

			if user is None:
				form.account.errors.append(u'존재하지 않는 아이디입니다.')
			elif (user.password != password):
				form.password.errors.append(u'비밀번호가 잘못되었습니다.')
			else:
				session.permanent = True
				session['admin'] = user.id
				return redirect(url_for('admin_main'))

			return render_template('main_admin.html', form=form)
		else:
			return render_template('main_admin.html', form=form)
	return render_template('main_admin.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = JoinForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			try:
				user = User(
						account = form.account.data,
						password = generate_password_hash(form.password.data),
						phone = form.phone.data,
						bank = form.bank.data,
						bank_account = form.bank_account.data,
						rec_person = form.rec_person.data,
						join_date = datetime.now()+timedelta(hours=9)
						)
				db.session.add(user)
				db.session.commit()

				return redirect(url_for('main'))
			except:
				flash(u'잘못된 DB접근.', u'DB 오류')
				return render_template('signup.html',form=form)

		return render_template('signup.html',form=form)
	else:
		return render_template('signup.html',form=form)

@app.route('/checkid', methods=['GET', 'POST'])
def check_id():
	if request.method == 'POST':
		check_id = request.form['id']
		if len(check_id) == 0:
			session['possiblejoin'] = False
			return jsonify(success = False, msg = u'확인하실 아이디를 입력하세요.')

		for ch in check_id:
			c = ord(ch)
			if (c >= 48 and c <= 57) or (c >= 65 and c <= 90) or (c >= 97 and c <= 122):
				continue;
			else:
				session['possiblejoin'] = False
				return jsonify(success = False, msg = u'알파벳 및 숫자만 가능합니다.')
		if check_id.isalnum():
			user = User.query.filter(User.account == check_id).first()
			if user is None:
				session['possiblejoin'] = True
				return jsonify(success = True, msg = u'사용가능한 아이디입니다.', test=session['possiblejoin'])
			else:
				session['possiblejoin'] = False
				return jsonify(success = False, msg = u'이미 존재하는 아이디입니다.')
		else:
			session['possiblejoin'] = False
			return jsonify(success = False, msg= u'사용불가한 문자가 포함되어있습니다.')
	else:
		return redirect(url_for('signup'))

@app.route('/signout')
def signout():
	session.clear()
	return redirect(url_for('betting_normal'))

####################################
############   admin   #############
####################################

# 로그인 후 메인 페이지
@app.route('/admin/main')
def admin_main():
	if 'admin' in session:
	#studies = Study.query.order_by(desc(Study.date_created)).all()
		user = User.query.filter(User.allow == 0).count()
		return render_template('admin/adminmain.html', user=user)
	else:
		return redirect(url_for('main'))

@app.route('/admin/control_user')
def admin_control_user():
	if 'admin' in session:
		user = User.query.filter(User.allow == 0).count()
		userlist = User.query.filter(User.allow == 0).all()
		return render_template('admin/control_user.html', user=user, userlist=userlist)
	else:
		return redirect(url_for('main'))

@app.route('/admin/schedule')
def admin_schedule():
	if 'admin' in session:
		user = User.query.filter(User.allow == 0).count()
		gamelist = Game.query.filter(Game.state == 0).all()
		return render_template('admin/schedule.html', menu="admin", user=user, gamelist = gamelist)
	else:
		return redirect(url_for('main'))

@app.route('/admin/addgame', methods=['GET', 'POST'])
def admin_addgame():
	if request.method == 'POST':
		print request.form['sport']
		print request.form['league']
		print request.form['home']
		print request.form['away']
		game = Game(
				#date=request.form['date'],
				sport=int(request.form['sport']),
				home=request.form['home'],
				away=request.form['away']
				)
		db.session.add(game)
		db.session.commit()
		
		return jsonify(success=True, id=game.id, sport=game.sport, home=game.home)
	return redirect(url_for('main'))
		
@app.route('/admin/league', methods=['GET', 'POST'])
def admin_league():
	if request.method == 'POST':
		sport = int(request.form['sport'])
		if sport == 0:
			msg = 'EPF'
		elif sport == 1:
			msg = 'MLB'
		else:
			msg ='NBA'
		return jsonify(success=True, msg=msg)
	return redirect(url_for('main'))

@app.route('/cross_betting')
def betting_normal():
	if 'id' in session:
	#studies = Study.query.order_by(desc(Study.date_created)).all()
		return render_template('betting_normal.html', menu="cross")
	elif 'admin' in session:
	#studies = Study.query.order_by(desc(Study.date_created)).all()
		user = User.query.filter(User.allow == 0).count()
		return render_template('betting_normal.html', menu="cross", user=user)
	else:
		return redirect(url_for('main'))



##############################
#########  게시판   ##########
##############################

@app.route('/article')
def article_list():
	# html 파일에 전달할 데이터 Context
	context = {}
	searchform = SearchForm()

	# Article 데이터 전부를 받아와서 최신글 순서대로 정렬하여 'article_list' 라는 key값으로 context에 저장한다.
	context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()
	return render_template('home.html', context=context,searchform=searchform)

@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
	form = ArticleForm()
	searchform = SearchForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
			article = Article(
					nick=form.nick.data,
					title=form.title.data,
					password=generate_password_hash(form.password.data),
					content=form.content.data,
					date_created=datetime.now()+timedelta(hours=9)
					)
			# 데이터베이스에 데이터를 저장
			db.session.add(article)
			db.session.commit()

			return redirect(url_for('article_list'))
		return render_template('article/create.html',searchform=searchform, form=form)

	return render_template('article/create.html',searchform=searchform, form=form)


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
	searchform = SearchForm()
	article = Article.query.get(id)

	# relationship을 활용한 query
	comments = article.comments.order_by(desc(Comment.date_created)).all()

	return render_template('article/detail.html',searchform=searchform, article=article, comments=comments)

@app.route('/article/like')
def article_like():
	id = int(request.args.get('id'))
	article = Article.query.get(id)
	article.like += 1

	db.session.commit()

	return jsonify(like=article.like)

@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
	article = Article.query.get(id)
	form = ArticleForm(request.form, obj=article)
	searchform = SearchForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			if check_password_hash(article.password, form.password.data):
				form.populate_obj(article)
				db.session.commit()
				return redirect(url_for('article_detail', id=id))
			else:
				return render_template('article/update.html',searchform=searchform, form=form, error=1)


	return render_template('article/update.html',searchform=searchform, form=form)


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
	searchform = SearchForm()
	if request.method == 'GET':
		return render_template('article/delete.html',searchform=searchform, article_id=id)
	elif request.method == 'POST':
		article_id = request.form['article_id']
		article = Article.query.get(article_id)
		if check_password_hash(article.password, request.form['password']):
			db.session.delete(article)
			db.session.commit()

			flash(u'게시글을 삭제하였습니다.', 'success')
			return redirect(url_for('article_list'))
		return render_template('article/delete.html',searchform=searchform, article_id=id)

@app.route('/article/search', methods=['GET'])
def article_search():
	searchform = SearchForm()
	if request.method == 'GET':
		search = request.args.get('search')	
		context = {}
		context['article_list'] = Article.query.filter(Article.title.contains(search)).order_by(desc(Article.date_created)).all()

		return render_template('home.html',searchform=searchform, context=context)
	else:
		return redirect(url_for('article_list'))
#
# @comment controllers
#
@app.route('/comment/create', methods=['GET', 'POST'])
def comment_create():
	if request.method == 'POST':
		#비번 해쉬로 해야할듯
		arc = Article.query.get(request.form['aid'])
		comment = Comment(
				nick=request.form['nick'],
				content=request.form['comment'],
				password=request.form['passwd'],
				article=arc,
				date_created=datetime.now()+timedelta(hours=9)
				)
		arc.nofc += 1
		db.session.add(comment)
		db.session.commit()

		return jsonify(success=True, id=comment.id, content=comment.content, nick=comment.nick, date_created=comment.date_created.isoformat())
	return redirect(url_for('article_list'))

@app.route('/comment/like/<int:id>', methods=['GET'])
def comment_like(id):
	comment = Comment.query.get(id)
	comment.like += 1

	db.session.commit()

	return redirect(url_for('article_detail', id=comment.article_id))

@app.route('/comment/delete', methods=['GET', 'POST'])
def comment_delete():
	searchform = SearchForm()
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



#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
	return render_template('500.html'), 500
