#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,TextAreaField, \
	DateTimeField,RadioField,SelectField,SelectMultipleField, \
	BooleanField
from wtforms.validators import Required,Length,Regexp

class UeditorForm(Form):
	title = StringField(u'标题：',validators=[Length(0,255)])
	editor1 = TextAreaField(u'内容：',id='editor')
	lead = TextAreaField(u'导语：',validators=[Length(0,255)])
	keywords = StringField(u'关键字：',validators=[Length(0,255)])
	auth  = StringField(u'作者：',validators=[Length(0,50)],default='hugesoft')
	src = StringField(u'来源：',validators=[Length(0,50)],default='hzrb')
	pub_time = DateTimeField(u'发布时间：', validators=[Required()])
	edit  = SelectField(u'编辑：',choices=[('0','mmx'),('1','mmx0087'),('2','hugesoft')], default='1' ,validators=[Required()])
	is_show = BooleanField(u'是否显示',default=True)
	
	submit = SubmitField(u'提交')