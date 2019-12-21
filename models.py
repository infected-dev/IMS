from . import db
from datetime import datetime
from flaskapp import app 

class Fabric(db.Model):
    __tablename__ = 'fabric'
    fid = db.Column(db.Integer, primary_key=True)
    fabric_name = db.Column(db.String(25), unique=True)
    def __init__(self,fabric_name): 
        self.fabric_name = fabric_name  


class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True)
    fabric_id = db.Column(db.Integer, db.ForeignKey('fabric.fid'))
    product_name = db.Column(db.String(100))
    designs = db.relationship('Design', backref='pduct', lazy=True)
    inventory = db.relationship('Inventory', backref='pduct', lazy=True)
    def __init__(self, fabric_id, product_name):
        
        self.fabric_id = fabric_id
        self.product_name = product_name

    def addDesign(self,num):
        design = Design(product_id = self.pid, design_no=int(num))
        db.session.add(design)
        db.session.commit()



    
    
class VariantMaster(db.Model):
    __tablename__ = 'variantmaster'

    vmid = db.Column(db.Integer, primary_key=True)
    variant_name = db.Column(db.String(20), unique=True)
    inventory_combine = db.relationship('Inventory', backref='variantname', lazy=True)

    def __init__(self, variant_name):
        self.variant_name = variant_name



    

class Design(db.Model):
    __tablename__ = 'design'

    did = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))
    design_no = db.Column(db.Integer)
    inventory = db.relationship('Inventory', backref='deno', lazy=True)

    def __init__(self,product_id, design_no):
        self.product_id = product_id
        self.design_no = design_no

    def addinventory(self,product_id, design_id,var_id):
        in_ven = Inventory(p_id=product_id, d_id=design_id, v_id=var_id, recieved=0, dispatched=0, currrent=0, uom='mtr')
        db.session.add(in_ven)
        db.session.commit()


class Operation(db.Model):
    __tablename__ = 'operation'

    oid = db.Column(db.Integer, primary_key=True)
    operation_name = db.Column(db.String(20), unique=True)
    logs = db.relationship('InventoryLog', backref='ops', lazy=True)


    def __init__(self, operation_name):
        self.operation_name = operation_name


class Inventory(db.Model):
    __tablename__ = 'inventory'

    iid = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('product.pid'))
    d_id = db.Column(db.Integer, db.ForeignKey('design.did'))
    v_id = db.Column(db.Integer, db.ForeignKey('variantmaster.vmid'))
    custom_id = db.Column(db.String(20), unique=True)
    recieved = db.Column(db.Float)
    dispatched = db.Column(db.Float)
    currrent = db.Column(db.Float)
    uom = db.Column(db.String(3), default='mtr')
    logs = db.relationship('InventoryLog', backref='main', lazy=True)


    def __init__(self,p_id, d_id,v_id, recieved, dispatched, currrent, uom):
        self.p_id = p_id
        self.d_id = d_id
        self.v_id = v_id
        self.recieved = 0
        self.dispatched = 0
        self.currrent = 0
        self.uom = uom


    def inward(self,date_time, i_id, o_id, inn):
        log = InventoryLog(date_time=datetime.now(), i_id=self.iid, o_id=1, quantity=inn, uom='mtr')
        db.session.add(log)
        self.recieved += inn
        db.session.commit()
    

    def outward(self,date_time, i_id, o_id, out):
        log = InventoryLog(date_time=datetime.now(), i_id=self.iid, o_id=2, quantity=out, uom='mtr')
        db.session.add(log)
        self.dispatched += out
        db.session.commit()
    

    def currentstock(self):
        self.current = self.recieved - self.dispatched
        db.session.commit()


class InventoryLog(db.Model):
    __tablename__ = 'inventorylog'

    ilog_id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    i_id = db.Column(db.Integer, db.ForeignKey('inventory.iid'))
    o_id = db.Column(db.Integer, db.ForeignKey('operation.oid'))
    quantity = db.Column(db.Float)
    uom = db.Column(db.String(3), default='mtr')


    def __init__(self, date_time, i_id, o_id, quantity, uom):
        self.date_time = date_time
        self.i_id = i_id
        self.o_id = o_id
        self.quantity = quantity
        self.uom = uom

