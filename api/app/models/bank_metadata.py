from app import db

class BankMetadata(db.Model):
    __tablename__ = 'BankMetadata'

    # Primary key
    BankID = db.Column(db.Integer, primary_key=True)

    # Additional columns
    AssociationCode = db.Column(db.Text)  # Association code
    AssociationName = db.Column(db.Text)  # Association name
    BankName = db.Column(db.Text)  # Bank name

    # Relationships
    invoicing = db.relationship('Invoicing', backref='bank_metadata', lazy=True)
    manual_eft = db.relationship('ManualEFT', backref='bank_metadata', lazy=True)
    chargeback = db.relationship('Chargeback', backref='bank_metadata', lazy=True)

    # Optional: String representation for debugging
    def __repr__(self):
        return (
            f"<BankMetadata(BankID={self.BankID}, AssociationCode={self.AssociationCode}, "
            f"AssociationName={self.AssociationName}, BankName={self.BankName})>"
        )
