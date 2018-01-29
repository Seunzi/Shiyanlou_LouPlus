#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template
import os,json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True



@app.route('/')
def index():
    filesdir = '/home/Seunzi-official/Code/files'
    filestitle = []
    for x in os.listdir(filesdir):
        filesname = filesdir + '/' + x
        with open(filesname,'r') as file:
            filesdict = json.loads(file.read())
            filestitle.append(filesdict['title'])

    return render_template('index.html',filestitle=filestitle)

@app.route('/files/<filename>')
def file(filename):
    filesdir = '/home/Seunzi-official/Code/files'
    filesname = filesdir + '/' + filename + '.json'
    filescontent = {}
    if os.path.isfile('filesname'):
        with open(filesname,'r') as file:
            filescontent = json.loads(file.read())
        return render_template('file.html',filescontent=filescontent)
    else:
        return render_template('404.html'),404


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()
