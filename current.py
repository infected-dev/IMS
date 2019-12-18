from flask import Flask, Blueprint, render_template, request, url_for

current = Blueprint('current', __name__)

@current.route('/current')
def main():
    return render_template('current.html')

