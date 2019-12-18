from flask import Flask, render_template, url_for, url_for, Blueprint

products = Blueprint('products', __name__)

@products.route('/products')
def main():
    return render_template('products.html')

