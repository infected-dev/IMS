from flask import Flask, render_template, url_for, url_for, Blueprint, request
from .models import Fabric, Product, Variation
from . import db

products = Blueprint('products', __name__)

@products.route('/products')
def main():
    variations = Variation.query.all()
    fabrics = Fabric.query.all()
    allproducts = Product.query.all()
    return render_template('products.html', variations=variations,
        fabrics=fabrics, allproducts=allproducts)

@products.route('/addFabrics', methods=['POST'])
def add_fabric():
    if request.form:
        fabric_name = request.form.get('fabric_name').title()
        f = Fabric.query.filter_by(fabric_name=fabric_name).first()
        if f:
            return {'status':'Already Created'}
        else:   
            fabric = Fabric(fabric_name = fabric_name)
            db.session.add(fabric)
            db.session.commit()
        return {'status':'Success'}


@products.route('/addVariations', methods=['POST'])
def add_variation():
    if request.form:
        variation = request.form.get('variation_name').title()
        v = Variation.query.filter_by(variation_name=variation).first()
        if v:
            return {'status':'Already Created'}
        else:
            var = Variation(variation_name=variation)
            db.session.add(var)
            db.session.commit()
            return {'status':'Success'}

@products.route('/addProducts', methods=['POST'])
def add_product():
    if request.form:
        f_id = request.form.get('fabric_select')
        product_name = request.form.get('product_name').title()
        p = Product.query.filter_by(product_name=product_name).first()
        if p:
            error = {'status':'Alreday Exists'}
            return error
        else:
            product = Product(fabric_id=f_id, product_name=product_name)
            db.session.add(product)
            db.session.commit()
            return {'status':'Success'}

@products.route('/addDesigns', methods=['POST'])
def add_designs():
    if request.form:
        product_id = request.form.get('product_name')
        p = Product.query.get(product_id)
        if p:
            p

        

