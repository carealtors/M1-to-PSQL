from app import db
from datetime import datetime

class DuesPayments(db.Model):
    __tablename__ = 'DuesPayments'

    # Composite primary key (MEMBER_ID, BILLING_YEAR, and LAST_CHANGED_DATETIME)
    MEMBER_ID = db.Column(db.BigInteger, nullable=False, primary_key=True)
    BILLING_YEAR = db.Column(db.Integer, nullable=False, primary_key=True)
    LAST_CHANGED_DATETIME = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, primary_key=True)

    # Additional columns
    MEMBER_FIRST_NAME = db.Column(db.Text)
    MEMBER_LAST_NAME = db.Column(db.Text)
    INCURRING_MEMBER_ID = db.Column(db.BigInteger)
    INCURRING_MEMBER_FIRST_NAME = db.Column(db.Text)
    INCURRING_MEMBER_LAST_NAME = db.Column(db.Text)
    PRIMARY_ASSOCIATION_ID = db.Column(db.Text)
    PRIMARY_STATE_ASSOCIATION_ID = db.Column(db.Text)
    BILLING_ASSOCIATION_ID = db.Column(db.BigInteger)
    OFFICE_ID = db.Column(db.BigInteger)
    PAYMENT_TYPE_CODE = db.Column(db.Text)
    PAYMENT_AMOUNT = db.Column(db.Numeric)
    CONTRIBUTION_TYPE_CODE = db.Column(db.Text)
    DUES_PAID_DATE = db.Column(db.Date)
    PAYMENT_SOURCE_CODE = db.Column(db.Text)
    EC_CONTROL_NUMBER = db.Column(db.Text)
    LAST_CHANGED_BY = db.Column(db.Text)

    # Optional: String representation for debugging
    def __repr__(self):
        return (
            f"<DuesPayments(MEMBER_ID={self.MEMBER_ID}, BILLING_YEAR={self.BILLING_YEAR}, "
            f"LAST_CHANGED_DATETIME={self.LAST_CHANGED_DATETIME}, PAYMENT_AMOUNT={self.PAYMENT_AMOUNT})>"
        )
