from app import db

class Invoicing(db.Model):
    __tablename__ = 'Invoicing'

    # Primary key
    InvoiceID = db.Column(db.Integer, primary_key=True)

    # Foreign key referencing BankMetadata
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))

    # Additional columns
    DestinationAssociation = db.Column(db.Text)  # Destination association
    ACHSettlementNumber = db.Column(db.Text)  # ACH Settlement number
    ECControlNumber = db.Column(db.Text)  # EC Control number
    MemberName = db.Column(db.Text)  # Member name
    MemberID = db.Column(db.BigInteger)  # Member ID (BigInteger for large integers)
    BillingYear = db.Column(db.Integer)  # Billing year
    GrossAmount = db.Column(db.Numeric)  # Gross amount
    AssociationPortion = db.Column(db.Numeric)  # Association's portion of the amount
    TransactionFee = db.Column(db.Numeric)  # Transaction fee
    NetAssociationPortion = db.Column(db.Numeric)  # Net association portion

    # Optional: String representation for debugging
    def __repr__(self):
        return (
            f"<Invoicing(InvoiceID={self.InvoiceID}, BankID={self.BankID}, "
            f"GrossAmount={self.GrossAmount}, MemberName={self.MemberName}, "
            f"BillingYear={self.BillingYear})>"
        )
