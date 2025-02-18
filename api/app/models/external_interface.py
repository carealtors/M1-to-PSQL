from app import db

class ExternalInterface(db.Model):
    __tablename__ = 'ExternalInterface'

    # Columns
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))  # Foreign key referencing BankMetadata
    DestinationAssociation = db.Column(db.Text)  # Destination association
    ACHSettlementNumber = db.Column(db.Text)  # ACH Settlement number
    EC_CONTROL_NUMBER = db.Column(db.Text)  # EC Control number
    MemberName = db.Column(db.Text)  # Member name
    MemberID = db.Column(db.BigInteger)  # Member ID (BigInteger for large integers)
    BillingYear = db.Column(db.Integer)  # Billing year
    GrossAmountOfInvoice = db.Column(db.Numeric)  # Gross amount of invoice
    AssociationPortionOfAmount = db.Column(db.Numeric)  # Association's portion of the amount
    TransactionFeeOnAssocPortion = db.Column(db.Numeric)  # Transaction fee on association portion
    NetAssociationPortion = db.Column(db.Numeric)  # Net association portion
    AccountName = db.Column(db.Text)  # Account name

    # Optional: String representation for debugging
    def __repr__(self):
        return (
            f"<ExternalInterface(BankID={self.BankID}, MemberName={self.MemberName}, "
            f"GrossAmountOfInvoice={self.GrossAmountOfInvoice}, BillingYear={self.BillingYear})>"
        )
