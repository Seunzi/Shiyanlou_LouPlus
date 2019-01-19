# Week 7 Building online educational website with Flask

<!-- TOC -->autoauto- [Week 7 Building online educational website with Flask](#week-7-building-online-educational-website-with-flask)auto    - [Render forms with macro](#render-forms-with-macro)auto            - [basic syntax](#basic-syntax)auto            - [Examples](#examples)auto    - [Custom forms' validator](#custom-forms-validator)auto            - [simple example](#simple-example)auto            - [basic syntax](#basic-syntax-1)auto    - [flask-login](#flask-login)autoauto<!-- /TOC -->

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

