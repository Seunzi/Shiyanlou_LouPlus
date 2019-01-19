"""app.py
Application Entry file
"""

import urllib
from rmon.app import create_app
from rmon.models import db

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database
    """
    print("sqlite3 database file is %s" % app.config['SQLALCHEMY_DATABASE_URI'])
    db.creat_all()


