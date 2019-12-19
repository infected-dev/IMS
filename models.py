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

    def addDesign(self,num, varid):
        design = Design(product_id = self.pid, design_no=int(num), variation_id=varid)
        db.session.add(design)
        db.session.commit()


class Design(db.Model):
    __tablename__ = 'design'

    did = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))
    design_no = db.Column(db.Integer)
    variation_id = db.Column(db.Integer, db.ForeignKey('variation.vid'))
    inventory = db.relationship('Inventory', backref='deno', lazy=True)

    def __init__(self,variation_id,  product_id, design_no):
        self.variation_id = variation_id
        self.product_id = product_id
        self.design_no = design_no

    


class Variation(db.Model):
    __tablename__ = 'variation'

    vid = db.Column(db.Integer, primary_key=True)
    variation_name = db.Column(db.String(50), unique=True)

    def __init__(self,variation_name):
        self.variation_name = variation_name

    def addVariation(self, name):
        var = Variation(variation_name=name)
        db.session.add(var)
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
    custom_id = db.Column(db.String(20), unique=True)
    recieved = db.Column(db.Float)
    dispatched = db.Column(db.Float)
    currrent = db.Column(db.Float)
    uom = db.Column(db.String(3), default='mtr')
    logs = db.relationship('InventoryLog', backref='main', lazy=True)


    def __init__(self,p_id, d_id,custom_id, recieved, dispatched, currrent, uom):
        self.p_id = p_id
        self.d_id = d_id
        self.custom_id = f"RP{self.p_id}D{self.d_id}I{self.iid}"
        self.recieved = recieved
        self.dispatched =dispatched
        self.currrent =currrent
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

