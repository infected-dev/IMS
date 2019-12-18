import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

from .current import current as current_blueprint
app.register_blueprint(current_blueprint)

from .products import products as products_blueprint
app.register_blueprint(products_blueprint)

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run()