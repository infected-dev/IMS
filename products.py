from flask import Flask, render_template, url_for, url_for, Blueprint, request,redirect,flash
from .models import Fabric, Product, Design, VariantMaster
from . import db

prod = Blueprint('products', __name__)

@prod.route('/products', methods=['GET','POST'])
def main():
    
    fabrics = Fabric.query.all()
    allproducts = Product.query.all()
    allvariants = VariantMaster.query.all()
    alldesings = ''
    if request.form:
        pid = int(request.form.get('product_select'))
        p = Product.query.get(pid)
        alldesings = p.designs
    return render_template('products.html',
                           fabrics=fabrics, allproducts=allproducts, alldesings=alldesings,
                           allvariants=allvariants)

@prod.route('/addFabrics', methods=['POST'])
def add_fabric():
    if request.form:
        fabric_name = request.form.get('fabric_name').title()
        f = Fabric.query.filter_by(fabric_name=fabric_name).first()
        if f:
            flash('Fabric Already Ceated', category='alert-danger')
            return redirect(url_for('products.main'))
        else:   
            fabric = Fabric(fabric_name = fabric_name)
            db.session.add(fabric)
            db.session.commit()
            flash('Fabric Created', category='alert-success')
        return redirect(url_for('products.main'))

@prod.route('/addProducts', methods=['POST'])
def add_product():
    if request.form:
        f_id = request.form.get('fabric_select')
        product_name = request.form.get('product_name').title()
        p = Product.query.filter_by(product_name=product_name).first()
        if p:
            flash('Product Already Created', category='alert-danger')
            return redirect(url_for('products.main'))
        else:
            product = Product(fabric_id=f_id, product_name=product_name)
            db.session.add(product)
            db.session.commit()
            flash('Product Created', category='alert-success')
            return redirect(url_for('products.main'))

@prod.route('/addDesigns', methods=['POST'])
def add_design():
    if request.form:
        pid = request.form.get('product_name')
        p = Product.query.get(pid)
        p1 = p.designs
        print(p1)
        des = [i.design_no for i in p1]
        print(des)
        if p:
            num = int(request.form.get('design_no'))
            if num in des:
                flash('Design Already Registered', category='alert-danger')
                return redirect(url_for('products.main'))
            else:
                p.addDesign(num)
                flash('Design Created', category='alert-success')
                return redirect(url_for('products.main'))

@prod.route('/addVaraints', methods=['POST'])
def add_variants():
    if request.form:
        v = request.form.get('variant_name').title()
        if v:
            vq = VariantMaster.query.filter_by(variant_name=v).first()
            if vq:
                flash(f'{vq.variant_name} is already Registered', category='alert-danger')
                return redirect(url_for('products.main'))
            else:
                v1 = VariantMaster(variant_name=v)
                db.session.add(v1)
                db.session.commit()
                flash(f'{v1.variant_name} Added to Master', category='alert-success')
                return redirect(url_for('products.main'))

@prod.route('/addItem', methods=['POST'])
def add_item():
    if request.form:
        design_no = request.form.get('design_select')
        d = Design.query.get(design_no)
        if d:
            vid = request.form.getlist('varaint_name')
            for v in vid:
                v = int(v)
                d.addinventory(product_id=d.product_id, design_id=d.did, var_id=v)
                flash(f'Added {d.pduct.product_name} DesNo {d.design_no}V{v}') 
            return redirect(url_for('products.main'))

        return redirect(url_for('products.main'))




        

    

        

