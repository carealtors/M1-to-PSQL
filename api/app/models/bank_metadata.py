from app import db

class BankMetadata(db.Model):
    __tablename__ = 'BankMetadata'

    BankID = db.Column(db.Integer, primary_key=True)
    BankName = db.Column(db.String)
    AssociationCode = db.Column(db.String)
    AssociationName = db.Column(db.String)
