from app import db

class ManualEFT(db.Model):
    __tablename__ = 'ManualEFT'

    EFTID = db.Column(db.Integer, primary_key=True)  # Primary Key
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))  # Foreign Key linking to BankMetadata
    Amount = db.Column(db.Numeric)  # EFT transaction amount
