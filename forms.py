# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SelectMultipleField, RadioField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class AdminForm(Form):
	account = StringField(
			u'아이디',
			[validators.data_required(u'관리자 아이디를 입력하세요.')],
			description={'placeholder': u'관리자 아이디'}
			)
	password = PasswordField(
			u'비밀번호',
			[validators.data_required(u'비밀번호를 입력 필요')],
			description={'placeholder': u'비밀번호 입력'}
			)

class LoginForm(Form):
	account = StringField(
			u'아이디',
			[validators.data_required(u'아이디을 입력하시기 바랍니다.')],
			description={'placeholder': u'아이디'}
			)
	password = PasswordField(
			u'비밀번호',
			[validators.data_required(u'비밀번호를 입력하시기 바랍니다.')],
			description={'placeholder': u'비밀번호'}
			)

class JoinForm(Form):
	account = StringField(
			u'아이디',
			[validators.data_required(u'아이디을 입력하시기 바랍니다.')],
			description={'placeholder': u'아이디'}
			)
	password = PasswordField(
			u'비밀번호',
			[validators.data_required(u'비밀번호를 입력하시기 바랍니다.'),validators.Length(min=6, max=20, message=u'6자리 이상 입력하세요.'),
				validators.EqualTo('confirm_password', message=u'비밀번호가 일치하지 않습니다.')],
			description={'placeholder': u'비밀번호'}
			)
	confirm_password = PasswordField(
			u'비밀번호 확인',
			[validators.data_required(u'비밀번호를 두번 입력해야 합니다.')],
			description={'placeholder': u'비밀번호 확인'}
			)
	nickname = StringField(
			u'닉네임',
			[validators.data_required(u'닉네임을 입력'),validators.Length(min=3, max=20)],
			description={'placeholder': u'닉네임'}
			)
	phone = StringField(
			u'전화번호',
			[validators.data_required(u'전화번호를 입력하시기 바랍니다.')],
			description={'placeholder': u'전화번호 (01012341234)'}
			)
	bank = SelectField(
			u'은행명', 
			choices=[('0',u'국민은행'),('1',u'신한은행'),('2',u'우리은행'), ('3',u'농협')]
			)
	bank_account = StringField(
			u'계좌번호',
			[validators.data_required(u'계좌번호를 입력하시기 바랍니다.')],
			description={'placeholder': u'계좌번호'}
			)
	bank_name = StringField(
			u'예금주',
			[validators.data_required(u'예금주를 입력하시기 바랍니다.'),validators.Length(min=3, max=5, message=u'이름이 잘못되었습니다.')],
			description={'placeholder': u'예금주'}
			)
	rec_person = StringField(
			u'추천인',
			[validators.data_required(u'추천인을 입력하시기 바랍니다.')],
			description={'placeholder': u'추천인'}
			)



class ArticleForm(Form):
	nick = StringField(
	    u'닉네임',
	    [validators.data_required(u'이름을 입력하시기 바랍니다.')],
	    description={'placeholder': u'이름을 입력하세요.'}
	)
	password = PasswordField(
			u'비밀번호',
			[validators.data_required(u'비밀번호를 입력해야 합니다.'),validators.Length(min=4, max=16)],
			description={'placeholder': u'비밀번호를 입력하세요.'}
			)
	title = StringField(
			u'제목',
			[validators.data_required(u'제목을 입력하시기 바랍니다.')],
			description={'placeholder': u'제목을 입력하세요.'}
			)
	content = TextAreaField(
			u'내용',
			[validators.data_required(u'내용을 입력하시기 바랍니다.')],
			description={'placeholder': u'내용을 입력하세요.'}
			)
	#category = StringField(
	#    u'카테고리',
	#    [validators.data_required(u'카테고리를 입력하시기 바랍니다.')],
	#    description={'placeholder': u'카테고리를 입력하세요.'}
	#)


class CommentForm(Form):
	content = StringField(
			u'내용',
			[validators.data_required(u'내용을 입력하시기 바랍니다.')],
			description={'placeholder': u'내용을 입력하세요.'}
			)
	#author = StringField(
	#    u'작성자',
	#    [validators.data_required(u'이름을 입력하시기 바랍니다.')],
	#    description={'placeholder': u'이름을 입력하세요.'}
	#)
	password = PasswordField(
			u'비밀번호',
			[validators.data_required(u'비밀번호를 입력하시기 바랍니다.'), validators.Length(min=4, max=16)],
			description={'placeholder': u'비밀번호를 입력하세요.'}
			)
	#email = EmailField(
	#    u'이메일',
	#    [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
	#    description={'placeholder': u'이메일을 입력하세요.'}
	#)


