#-*- coding: utf-8 -*-
import os
import re
import json
import time

from flask import render_template, url_for,make_response,request
from . import admin
from .. import app
from .. import db
from ..models import Content
from uploader import Uploader
from Forms import UeditorForm
from flask import redirect
from flask.ext.moment import Moment

@admin.route('/content/',methods=['GET','POST'])
def add_content():
    form = UeditorForm()
#    tm = time.strftime("%Y-%m-%d %H:%M:%S")
#    print '%s ' % tm
    form.pub_time.data = time

    if form.validate_on_submit():
        content =Content(title=form.title.data,content=form.editor1.data,
            editor=form.edit.data)

        db.session.add(content)
        db.session.commit()
        return redirect(url_for('admin.update_content',id=content.id))

    return render_template('content/content.html',form=form)
    
@admin.route('/content/<id>',methods=['GET','POST'])
def update_content(id):
    form = UeditorForm()
    content = Content.query.get(int(id))
    
    if form.validate_on_submit(): 
        content.content = form.editor1.data
        content.title = form.title.data
        content.pub_time = form.pub_time.data
        content.editor = form.edit.data

        db.session.add(content)
        db.session.commit()            
    else:
        form.editor1.data = content.content
        form.title.data = content.title
        form.pub_time.data = content.pub_time
        form.edit.data = content.editor

    return render_template('content/content.html',form=form)

@admin.route('/list/<b_id>,<s_id>', methods=['GET','POST'])
def list_title(b_id, s_id):
    list = db.session.query(Content.id,Content.title, \
        Content.content,Content.modity_time,Content.editor). \
        filter_by(big_class_id=b_id,small_class_id=s_id).all()

    return render_template('content/list_admin.html',title=list)

@admin.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口

    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
       
    action = request.args.get('action')

    # 解析JSON格式的配置文件
    with open(os.path.join(app.static_folder,'ueditor','php','config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}
                
    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }

        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']

        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)

        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })

        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list

    else:
        result['state'] = '请求地址出错'

    result = json.dumps(result)

    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})

    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res


#init DB

@admin.route('/createdb')
def createdb():
    db.create_all()
    
    test_content = Content(title = 'hugesoft', content = 'Hello World!')
    db.session.add(test_content)
    db.session.commit()
    
    return render_template('user.html', name = 'create_all')

@admin.route('/drop')
def drop_all():
    db.drop_all()
    return  render_template('user.html', name = 'drop_all')
