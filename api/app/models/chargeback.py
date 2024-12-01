from app import db

class Chargeback(db.Model):
    __tablename__ = 'Chargeback'

    ChargebackID = db.Column(db.Integer, primary_key=True)  # Primary Key
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))  # Foreign Key linking to BankMetadata
    Amount = db.Column(db.Numeric)  # Chargeback amount
