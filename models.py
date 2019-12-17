from . import db
from datetime import datetime
from flaskapp import app 

class Brand(db.Model):
    __tablename__ = "brand"

    brand_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(30))
    products = db.relationship('Product', backref='brand')

class Product(db.Model):
    __tablename__ = "product"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(25))
    design_no = db.Column(db.Integer)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.brand_id'))
    log_date = db.Column(db.Date, default=datetime.now().date())
    inventory = db.relationship('Inventory', uselist=False, backref='product')

class Inventory(db.Model):
    __tablename__='inventory'

    inventory_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    initial_qty = db.Column(db.Integer, default = 0)
    inward_qty = db.Column(db.Integer) 
    outward_qty = db.Column(db.Integer)
    logsheet = db.relationship('InventoryLog', backref='mainlog')
    
class InventoryLog(db.Model):
    __tablename__='inventorylog'

    inventorylog_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.prodcut_id'))
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'))
    operation_id = db.Column(db.Integer, db.ForeignKey('operation.oid'))
    quantity  = db.Column(db.Integer)
    log_date = db.Column(db.Date, defualt=datetime.now())

class operation(db.Model):
    __tablename__ = 'operation'

    oid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

