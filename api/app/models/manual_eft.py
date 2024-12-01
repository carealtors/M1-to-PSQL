from app import db

class ManualEFT(db.Model):
    __tablename__ = 'ManualEFT'

    # Primary key
    EFTID = db.Column(db.Integer, primary_key=True)

    # Foreign key referencing BankMetadata
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))

    # Additional columns
    ReceivingAssociation = db.Column(db.Text)  # Receiving association
    ACHSettlementNumber = db.Column(db.Text)  # ACH Settlement number
    ECControlNumber = db.Column(db.Text)  # EC Control number
    DestinationOrganization = db.Column(db.Text)  # Destination organization
    Amount = db.Column(db.Numeric)  # Amount

    # Optional: String representation for debugging
    def __repr__(self):
        return (
            f"<ManualEFT(EFTID={self.EFTID}, BankID={self.BankID}, "
            f"Amount={self.Amount}, ReceivingAssociation={self.ReceivingAssociation})>"
        )
