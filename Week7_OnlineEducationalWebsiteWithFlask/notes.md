# Week 7 Building online educational website with Flask

- [Week 7 Building online educational website with Flask](#week-7-building-online-educational-website-with-flask)
  - [Get ready to code](#get-ready-to-code)
  - [Backend modularity](#backend-modularity)
  - [Blueprint](#blueprint)
  - [Updating `User` model with `werkzeug`](#updating-user-model-with-werkzeug)
  - [flask-migrate](#flask-migrate)
  - [Creating sign up and sign in forms](#creating-sign-up-and-sign-in-forms)
      - [flask-wtf](#flask-wtf)
      - [simple usage](#simple-usage)
  - [Render forms with macro](#render-forms-with-macro)
      - [basic syntax](#basic-syntax)
      - [Examples](#examples)
  - [Custom forms' validator](#custom-forms-validator)
      - [simple example](#simple-example)
      - [basic syntax](#basic-syntax-1)
  - [flask-login](#flask-login)
      - [Login example](#login-example)
      - [Logout example](#logout-example)
  - [Render forms' error message](#render-forms-error-message)
      - [Render example](#render-example)
  - [Flash messages](#flash-messages)
      - [Example with Bootstrap](#example-with-bootstrap)

## Get ready to code

Install `flask` and `flask-sqlalchemy`  

Configure the mysql server in `/etc/mysql/my.cnf`:

```ini
[client]
default-character-set = utf8

[mysqld]
character-set-server = utf8

[mysql]
default-character-set = utf8
```

Start the mysql server and create the database  

```bash
$ sudo service mysql start
$ mysql -uroot

mysql> CREATE DATABASE simpledu;
```

## Backend modularity

File structure

```bash
simpledu/
    __init__.py # required to been a python package
    config.py   # for configurations
    models.py   # for data models
    forms.py    # for forms
    app.py      # create and configure the Flask app
```

Modify the configurations in `config.py` that can be use to variety of environment

```python
class BaseConfig(object):
  """ Base class of configuration """
  SECRET_KEY = 'makesure to set a very secret key'

class DevelopmentConfig(BaseConfig):
  """ Configuration for developing """
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/simpledu?charset=utf8'

class ProductionConfig(BaseConfig):
  """ Configuration for producing """
  pass

class TestingConfig(BaseConfig):
  """ Configuration for testing """
  pass

configs = {
  'development' : DevelopmentConfig,
  'production' : ProductionConfig,
  'testing' : TestingConfig
}
```

Build the factory function in `app.py` in order to create and configure the Flask app

```python
from flask import Flask
from simpledu.config import configs
from simpledu.models import db, Course

def create_app(config):
  """ loading configuration by the name """
  app = Flask(__name__)
  app.config.from_object(configs.get(config))
  # initiate the SQLAlchemy by init_app
  db.init_app(app)
  ...
```

Using `create_app` in `manage.py`

```python
from simpledu.app import create_app

# for developing
app = create_app('development')

if __name__ == '__main__':
  app.run()
```

## Blueprint

Flask uses a concept of *blueprints* for making application components and supporting common patterns within an application or across applications.

Make a directory `handlers` for blueprints

```bash
handlers/
  __init__.py
  front.py
  course.py
  admin.py
```

Create Blurprint in each file  
Example:

```python
from flask import Blueprint
# omit url_prefix means the Blueprint is on root
# front.py
front = Blueprint('front', __name__)
# course.py
course = Blueprint('course', __name__, url_prefix='/courses')
```

Import the Blueprints in `__init__.py`

```python
from .front import front
from .course import course
from .admin import admin
```

Register the Blueprints in `app.py`

```python
...
def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
...
# adding register function to create_app
def create_app(config):
    ...
    register_blueprints(app)
    ...
```

## Updating `User` model with `werkzeug`

User model code:

```python
from werzeug.security import generate_password_hash, check_password_hash

class User(Base):
  __tablename__ = 'user'
  ...
  # set the password as private
  _password = db.Column('passowrd', db.String(256), nullable=False)
  ...
  @property
  def password(self):
      """ getter """
      return self._password
  
  @password.setter
  def password(self, orig_password):
      """ setter, so that the password will automatically change into hash value and saved to _password """
      self._password = generate_password_hash(orig_password)
  
  def check_password(self, password):
      """ check the input password with stored password in hash """
      return check_password_hash(self._password, passowrd)
```

## flask-migrate

Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.  

Register to the applications in `app.py`

```python
from flask_migrate import Migrate

def create_app(config):
    """App factory"""
    ...
    Migrate(app,db)
    ...
```

run `flask db` to check if configure properly  

Initiation `flask db init`  

Migrate database with message `flask db migrate -m 'init database'`  

Upgrade the database `flask db upgrade`  


## Creating sign up and sign in forms

#### flask-wtf

`wtfroms` is a python package for mapping HTML forms to Python object, like a ORM.  
`flask-wtf` is a integration of Flask and WTForms, including CSRF, file upload, and reCAPTCHA.

#### simple usage

```python
from flask_wtf import FlaskForm
from wtfroms import StringField
from wtfroms.validators import DataRequired

class MyForm(FlaskForm):
  name = StringField('name', validators=[DataRequired()])

```

For each input in From class, you need to declare the corresponding Field.  
Field have two parameters, first one for HTML label, second one for validators.  

You can also custom error messages in validator like:

```python
Email(message='Please input the correct email address')
```

## Render forms with macro

Using jinja2 `macro` to encapsulate codes for reusing.

#### basic syntax

Define a macro

```
{% macro macro_name(arg1, arg2, ...) %}
...
{% endmacro %}
```

Import macro in templates

```
{% from "macros.html" import macro_name %}
```

Call the macro

```
{{ macro_name(arg1, arg2, ...) }}
```

#### Examples

```html
{% macro render_form(form, url) %}
<form method="POST" action="{{ url }}">
  <!-- start with csrf_token rendering -->
  {{ form.csrf_toekn }}
  <!-- render every forms' field -->
  {% for field in form %}
    <!-- no render csrf_token field -->
    {% if field.type == 'CSRFTokenField' %}
    {{ '' }}
    <!-- handle SubmitField -->
    {% elif field.type == 'SubmitField' %}
    {{ form.submit(class='btn btn-primary', type='submit') }}
    <!-- handle BooleanField -->
    {% elif field.type == 'BooleanField' %}
    <div class="checkbox">
      <label>{{ field() }} {{ field.label.text }}</label>
    </div>
    {% else %}
    <div class="from-group">
      {{ field.label }} {{ field(class='from-control') }}
    </div>
    {% endif %}
  {% endfor %}
</form>
{% endmacro %}
```

## Custom forms' validator

#### simple example

```python
from wtfroms import ValidationError

class NameFrom(FlaskForm):
    name = StringField('Your name')

    def validate_name(self, field):
        if len(field.data) < 2:
            raise ValidationError('Length of name can not less than 2')
```

#### basic syntax

```python
# inside FlaskFrom class:
# call validator when submit the froms
def validate_fieldname(self, field):
    # using field.data to access data
    # raise ValidationError after field.data validation failed
```

## flask-login

`flask-login` provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users' sessions over extended periods time.

Update your user model class with `UserMixin` base class in order to use `is_authenticated` property to check user if login.  

Configuring Application in `app.py` :

```python
...
login_manager = LoginManager()
login_manager.init_app(app)

# Provide a user_loader callback.
# It's used to reload the user object from the user ID stored in the session.
# It should take the unicode ID of a user, and reutrn the corresponding user object.
@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)

login_manager.login_view = 'front.login'
...
```

#### Login example

```python
from flask_login import login_user

@front.route('/login',methods=['GET','POST'])
def login():
    from = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html',form=form)
```

#### Logout example

```python
from flask_login import login_user, logout_user, login_required

@front.route('./logout')
@login_required
def logout():
    logout_user()
    flash('Logout success','success')
    return redirect(url_for('.index'))
```

## Render forms' error message

Each Field of form class has a `errors` value, it initiate with a empty list, means no errors.
When `form.validate_on_submit` fail, the error message will be added to the list.

#### Render example

```html
<!-- When errors not empty, add class has-error to div tag, so the input form will turn red -->
<div class="from-group {% if field.errors %}has-error{% endif %}">
  {{ field.label }} {{ field(class='form-control') }}
<!-- When errors not empty, iterate each error message -->
  {% if field.errors %}
    {% for error in field.errors %}
    <!-- Bootstrap style -->
    <span class="help-block">{{ error }}</span>
    {% endfor %}
  {% endif %}
</div>
```

## Flash messages

Using `get_flashed_message()` in jinja2 to receive the flashed messages.

#### Example with Bootstrap
```html
<div class="container">
  {% with messages = get_flashed_message(with_categories=true) %}
    {% if messages %}
    {% for category, message in messages %}
    <div class="alert alert-{{ category }} alert-dismissible" role="alert">
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="ture">&times;</span>
      </button>
      {{ message }}
    </div>
    {% endfor %}
    {% endif %}
  {% endwith %}
</div>