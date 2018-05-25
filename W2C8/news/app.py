#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import os,json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)
client = MongoClient('127.0.0.1',27017)
db1 = client.shiyanlou

class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('files',lazy='dynamic'))
    content = db.Column(db.Text)

    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return self.title

    def add_tag(self,tag_name,db1=db1):
        if db1.files.find_one({'file_id':self.id}).count()!=0:
            db1.files.update({'file_id':self.id},{'$addToSet':{'tag':[tag_name]}})
        else:
            tag = {'file_id':self.id,'tag':tag_name}
            db1.files.insert_one(tag)
        pass

    def remove_tag(self,tag_name,db1=db1):
        if db1.files.find_one({'file_id':self.id,'tag':tag_name}).count()!=0:
            db1.files.deleteOne({'file_id':self.id,'tag':tag_name})
        pass

    @property
    def tags(self,db1=db1):
        tagstrings = ''
        if db1.files.find_one({'file_id':self.id,'tag':{'$exists':True}}).count()!=0:
            for file in db1.files.find_one({'file_id':self.id}):
                tagstrings = ','.join(file['tag'])
        return tagstrings

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name

@app.route('/')
def index():
    files1 = File.query.all()
    return render_template('index.html',files=files1)

@app.route('/files/<file_id>')
def file(file_id):
    file1 = File.query.filter_by(id=file_id).first()
    if file1:
        return render_template('file.html',files=file1)
    else:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()
