from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class DuesPaymentsSummary(db.Model):
    __tablename__ = 'dues_payments_summary'  # Matches the view name in PostgreSQL

    billing_association_id = db.Column("BILLING_ASSOCIATION_ID", db.String, primary_key=True)
    association_name = db.Column("ASSOCIATION_NAME", db.String)
    null_ec_control_number = db.Column("null_ec_control_number", db.Integer)
    total_payments = db.Column("total_payments", db.Integer)
    ec_percentage = db.Column("ec_percentage", db.Float)

    def __repr__(self):
        return (
            f"<DuesPaymentsSummary("
            f"billing_association_id='{self.billing_association_id}', "
            f"association_name='{self.association_name}', "
            f"ec_percentage={self.ec_percentage})>"
        )
