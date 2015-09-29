from app import db


class PC(db.Model):
    tablename__ = 'PC'
    id = db.Column(db.Integer, primary_key=True)
    CPU = db.Column(db.String(64))
    RAM = db.Column(db.Integer)
    HDD = db.Column(db.Integer)
    MB = db.Column(db.String(64))
    video = db.Column(db.String(64))
    assembly_by = db.Column(db.String(64))
    assembly_time = db.Column(db.DateTime)
    approved_by = db.Column(db.String(64))
    approved_time = db.Column(db.DateTime)
    reserved_time = db.Column(db.DateTime)
    sale_time = db.Column(db.DateTime)
    buyer = db.Column(db.String(64))
    status_id = db.Column(db.Integer, db.ForeignKey('item_status.id'))
    status = db.relationship("ItemStatus", backref="PC")
    price = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    sold_by = db.Column(db.String(64))

    def __repr__(self):
        return '<PC %r>' % self.CPU


class Monitor(db.Model):
    tablename__ = 'Monitor'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(64))
    monitor_model = db.Column(db.String(64))
    size = db.Column(db.Integer)
    assembly_by = db.Column(db.String(64))
    assembly_time = db.Column(db.DateTime)
    approved_by = db.Column(db.String(64))
    approved_time = db.Column(db.DateTime)
    reserved_time = db.Column(db.DateTime)
    sale_time = db.Column(db.DateTime)
    buyer = db.Column(db.String(64))
    status_id = db.Column(db.Integer, db.ForeignKey('item_status.id'))
    status = db.relationship("ItemStatus", backref="Monitor")
    price = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    sold_by = db.Column(db.String(64))

    def __repr__(self):
        return '<Monitor %r>' % self.manufacturer


class ItemStatus(db.Model):
    tablename__ = 'item_status'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<ItemStatus %r>' % self.description


class User(db.Model):
    tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500))
    username = db.Column(db.String(64))
    dn = db.Column(db.String(500))
