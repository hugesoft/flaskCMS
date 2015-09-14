#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,DateTimeField,RadioField
from wtforms.validators import Required,Length,Regexp

class UeditorForm(Form):
	title = StringField(u'标题：',validators=[Length(0,255)])
	lead = TextAreaField(u'导语：',validators=[Length(0,255)])
	keywords = StringField(u'关键字：',validators=[Length(0,255)])
	auth  = StringField(u'作者：',validators=[Length(0,20)])
	scr = StringField(u'来源：',validators=[Length(0,50)])
	modiy_time = DateTimeField(u'时间：')
	editor1 = TextAreaField(id='editor')
	is_show = RadioField(u'是否显示')
	submit = SubmitField(u'提交')