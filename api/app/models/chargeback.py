from app import db

class Chargeback(db.Model):
    __tablename__ = 'Chargeback'

    # Primary key
    ChargebackID = db.Column(db.Integer, primary_key=True)

    # Foreign key referencing BankMetadata
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))

    # Additional columns
    ECControlNumber = db.Column(db.Text)  # EC Control number
    TransactionNumber = db.Column(db.Text)  # Transaction number
    DestinationOrganization = db.Column(db.Text)  # Destination organization
    Amount = db.Column(db.Numeric)  # Amount

    # Optional: String representation for debugging
    def __repr__(self):
        return (
            f"<Chargeback(ChargebackID={self.ChargebackID}, BankID={self.BankID}, "
            f"Amount={self.Amount}, ECControlNumber={self.ECControlNumber})>"
        )
