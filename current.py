from flask import Flask, Blueprint, render_template, request, url_for
from .models import Inventory

current = Blueprint('current', __name__)

@current.route('/current')
def main():
    allinventory = Inventory.query.all()
    return render_template('current.html', allinventory=allinventory)

