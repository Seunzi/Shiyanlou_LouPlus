from flask import Blueprint, render_template, flash, redirect, url_for
from simpledu.decorators import admin_required
from simpledu.forms import MessageForm
import json
import redis

live = Blueprint('live', __name__, url_prefix='/live')
redis = redis.from_url('redis://127.0.0.1:6379')


@live.route('/')
def index():
    return render_template('live/index.html')

@live.route('/systemmessage',methods=['POST'])
@admin_required
def systemmessage():
    form = MessageForm()
    if form.validate_on_submit():
        message = json.dumps(dict(username='System',text=str(form.message.data)))
        redis.publish('chat',message)
        flash('Message send','success')
        return redirect(url_for('admin.message'))
