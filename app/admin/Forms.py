#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,TextAreaField, \
	DateTimeField,RadioField,SelectField,SelectMultipleField, \
	BooleanField
from wtforms.validators import Required,Length,Regexp

class UeditorForm(Form):
	title = StringField(u'标题：',validators=[Length(0,255)])
	lead = TextAreaField(u'导语：',validators=[Length(0,255)])
	keywords = StringField(u'关键字：',validators=[Length(0,255)])
	auth  = StringField(u'作者：',validators=[Length(0,50)])
	src = StringField(u'来源：',validators=[Length(0,50)])
	modiy_time = DateTimeField(u'编辑时间：')
	editor1 = TextAreaField(u'内容：',id='editor')
	edit  = SelectField(u'编辑：',choices=[(1,'mmx'),(2,'hugesft'),(3,'mmx0087')],default=[2])
	is_show = BooleanField(u'是否显示',default=True)
	submit = SubmitField(u'提交')