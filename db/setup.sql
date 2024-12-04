-- Create the DuesPayments table
CREATE TABLE "DuesPayments" (
    "MEMBER_ID" BIGINT,
    "MEMBER_FIRST_NAME" TEXT,
    "MEMBER_LAST_NAME" TEXT,
    "INCURRING_MEMBER_ID" BIGINT,
    "INCURRING_MEMBER_FIRST_NAME" TEXT,
    "INCURRING_MEMBER_LAST_NAME" TEXT,
    "PRIMARY_ASSOCIATION_ID" TEXT,
    "PRIMARY_STATE_ASSOCIATION_ID" TEXT,
    "BILLING_ASSOCIATION_ID" BIGINT,
    "OFFICE_ID" BIGINT,
    "PAYMENT_TYPE_CODE" TEXT,
    "BILLING_YEAR" INTEGER,
    "PAYMENT_AMOUNT" NUMERIC,
    "CONTRIBUTION_TYPE_CODE" TEXT,
    "DUES_PAID_DATE" DATE,
    "PAYMENT_SOURCE_CODE" TEXT,
    "EC_CONTROL_NUMBER" TEXT,
    "LAST_CHANGED_BY" TEXT,
    "LAST_CHANGED_DATETIME" TIMESTAMP
);

-- Add indexes
-- CREATE INDEX "idx_duespayments_member_id" ON "DuesPayments" ("MEMBER_ID");
-- CREATE INDEX "idx_duespayments_office_id" ON "DuesPayments" ("OFFICE_ID");
-- CREATE INDEX "idx_duespayments_billing_year_payment_type" ON "DuesPayments" ("BILLING_YEAR", "PAYMENT_TYPE_CODE");

-- Create the MemberExtract table
CREATE TABLE "MemberExtract" (
    "MEMBER_ID" BIGINT PRIMARY KEY,
    "LAST_NAME" TEXT,
    "FIRST_NAME" TEXT,
    "MIDDLE_NAME" TEXT,
    "PRIMARY_LOCAL_ASSOCIATION_ID" BIGINT,
    "PRIMARY_STATE_ASSOCIATION_ID" BIGINT,
    "PRIMARY_OFFICE_ID" BIGINT,
    "MEMBER_TYPE_CODE" TEXT,
    "JOINED_DATE" DATE,
    "LOCAL_JOIN_DATE" DATE,
    "MEMBER_STATUS_CODE" TEXT,
    "MEMBER_STATUS_DATE" DATE,
    "PRIMARY_RE_LICENSE_NUMBER" TEXT,
    "PRIMARY_RE_LICENSE_STATE" TEXT,
    "HOME_ADDRESS_LINE_1" TEXT,
    "HOME_ADDRESS_LINE_2" TEXT,
    "HOME_ADDRESS_CITY" TEXT,
    "HOME_ADDRESS_STATE" TEXT,
    "HOME_ADDRESS_ZIP" TEXT,
    "HOME_ADDRESS_ZIP6" TEXT,
    "MAILING_ADDRESS_LINE_1" TEXT,
    "MAILING_ADDRESS_LINE_2" TEXT,
    "MAILING_ADDRESS_CITY" TEXT,
    "MAILING_ADDRESS_STATE" TEXT,
    "MAILING_ADDRESS_ZIP" TEXT,
    "MAILING_ADDRESS_ZIP6" TEXT,
    "CELL_PHONE" TEXT,
    "HOME_PHONE" TEXT,
    "DIRECT_DIAL" TEXT,
    "PERSONAL_FAX" TEXT,
    "BUSINESS_EMAIL_ADDRESS" TEXT,
    "BUSINESS_EMAIL_VERIFIED_FLAG" TEXT,
    "PERSONAL_EMAIL_ADDRESS" TEXT,
    "PERSONAL_EMAIL_VERIFIED_FLAG" TEXT,
    "TEAM_EMAIL_ADDRESS" TEXT,
    "SHARED_EMAIL_ADDRESS" TEXT,
    "SHARED_EMAIL_VERIFIED_FLAG" TEXT,
    "DESIGNATED_REALTOR_FLAG" TEXT,
    "GENERATION" TEXT,
    "NICKNAME" TEXT,
    "TITLE" TEXT,
    "GENDER" TEXT,
    "PREFERRED_PRONOUN" TEXT,
    "BIRTH_DATE" DATE,
    "ORIENTATION_DATE" DATE,
    "PREFERRED_MAIL_TYPE_CODE" TEXT,
    "PREFERRED_PUBLICATION_TYPE_CODE" TEXT,
    "PREFERRED_PHONE_TYPE_CODE" TEXT,
    "PREVIOUS_NON_MEMBER_FLAG" TEXT,
    "STOP_PUBLICATION_FLAG" TEXT,
    "SINGLE_OWNED_MLS_STATUS_CODE" TEXT,
    "SINGLE_OWNED_MLS_STATUS_DATE" DATE,
    "MEMBER_PRIMARY_IND" TEXT,
    "ALC_STATUS" TEXT,
    "ALC_DATE" DATE,
    "PMN_STATUS" TEXT,
    "PMN_DATE" DATE,
    "GREEN_STATUS" TEXT,
    "GREEN_DATE" DATE,
    "ABRM_STATUS" TEXT,
    "ABRM_DATE" DATE,
    "GAA_STATUS" TEXT,
    "GAA_DATE" DATE,
    "CRB_STATUS" TEXT,
    "CRB_DATE" DATE,
    "SRS_STATUS" TEXT,
    "SRS_DATE" DATE,
    "CRS_STATUS" TEXT,
    "CRS_DATE" DATE,
    "GRI_STATUS" TEXT,
    "GRI_DATE" DATE,
    "SRES_STATUS" TEXT,
    "SRES_DATE" DATE,
    "CIPS_STATUS" TEXT,
    "CIPS_DATE" DATE,
    "RCE_STATUS" TEXT,
    "RCE_DATE" DATE,
    "CRE_STATUS" TEXT,
    "CRE_DATE" DATE,
    "RAA_STATUS" TEXT,
    "RAA_DATE" DATE,
    "SIOR_STATUS" TEXT,
    "SIOR_DATE" DATE,
    "ARM_STATUS" TEXT,
    "ARM_DATE" DATE,
    "CCIM_STATUS" TEXT,
    "CCIM_DATE" DATE,
    "CPM_STATUS" TEXT,
    "CPM_DATE" DATE,
    "ABR_STATUS" TEXT,
    "ABR_DATE" DATE,
    "SPECIAL_DISCOUNT_FLAG" TEXT,
    "PRIMARY_FIELD_OF_BUSINESS" TEXT,
    "SECONDARY_FIELD_OF_BUSINESS1" TEXT,
    "SECONDARY_FIELD_OF_BUSINESS2" TEXT,
    "SECONDARY_FIELD_OF_BUSINESS3" TEXT,
    "WEBPAGE_ADDRESS" TEXT,
    "MLS" TEXT,
    "ARBITRATION_ETHICS_PENDING" TEXT,
    "STOP_FAX_FLAG" TEXT,
    "OFFICE_VOICEMAIL_EXTENSION_NUMBER" TEXT,
    "REINSTATEMENT_CODE" TEXT,
    "REINSTATEMENT_DATE" DATE,
    "MEMBER_SUBCLASS" TEXT,
    "STOP_EMAIL_FLAG" TEXT,
    "STOP_MAIL_FLAG" TEXT,
    "OCCUPATION_NAME" TEXT,
    "DIRECT_MARKETING_FLAG" TEXT,
    "DUES_WAIVED_LOCAL_FLAG" TEXT,
    "DUES_WAIVED_STATE_FLAG" TEXT,
    "DUES_WAIVED_NATIONAL_FLAG" TEXT,
    "LOCAL_SUSPENSION_FLAG" TEXT,
    "LAST_CHANGED_BY" TEXT,
    "LAST_CHANGED_DATETIME" TIMESTAMP
);

-- Add indexes
CREATE INDEX "idx_memberextract_office_id" ON "MemberExtract" ("PRIMARY_OFFICE_ID");
CREATE INDEX "idx_memberextract_member_status" ON "MemberExtract" ("MEMBER_STATUS_CODE");

-- Create the MemberSecondaryExtract table
CREATE TABLE "MemberSecondaryExtract" (
    "MEMBER_ID" BIGINT,
    "ASSOCIATION_ID" BIGINT,
    "OFFICE_ID" BIGINT,
    "LOCAL_JOIN_DATE" DATE,
    "MEMBER_STATUS_CODE" TEXT,
    "MEMBER_STATUS_DATE" DATE,
    "RE_LICENSE_NUMBER" TEXT,
    "LICENSE_STATE" TEXT,
    "MEMBER_SUBCLASS" TEXT,
    "MEMBER_TYPE_CODE" TEXT,
    "ARBITRATION_ETHICS_PENDING" TEXT,
    "DUES_WAIVED_FLAG" TEXT,
    "SPECIAL_DISCOUNT_FLAG" TEXT,
    "LAST_CHANGED_BY" TEXT,
    "LAST_CHANGED_DATETIME" TIMESTAMP
);

-- Add indexes to optimize queries
CREATE INDEX "idx_membersecondary_member_id" ON "MemberSecondaryExtract" ("MEMBER_ID");
CREATE INDEX "idx_membersecondary_office_id" ON "MemberSecondaryExtract" ("OFFICE_ID");
CREATE INDEX "idx_membersecondary_association_status" ON "MemberSecondaryExtract" ("ASSOCIATION_ID", "MEMBER_STATUS_CODE");
CREATE INDEX "idx_membersecondary_license_number" ON "MemberSecondaryExtract" ("RE_LICENSE_NUMBER");
CREATE INDEX "idx_membersecondary_status_date" ON "MemberSecondaryExtract" ("MEMBER_STATUS_DATE");

-- Create the OfficeExtract table
CREATE TABLE "OfficeExtract" (
    "OFFICE_ID" BIGINT PRIMARY KEY,
    "PRIMARY_LOCAL_ASSOCIATION_ID" BIGINT,
    "PRIMARY_STATE_ASSOCIATION_ID" BIGINT,
    "OFFICE_BUSINESS_NAME" TEXT,
    "JOINED_DATE" DATE,
    "OFFICE_STATUS_CODE" TEXT,
    "OFFICE_STATUS_DATE" DATE,
    "STREET_ADDRESS_LINE_1" TEXT,
    "STREET_ADDRESS_LINE_2" TEXT,
    "STREET_CITY" TEXT,
    "STREET_STATE" TEXT,
    "STREET_ZIP" TEXT,
    "STREET_ZIP6" TEXT,
    "MAILING_ADDRESS_LINE_1" TEXT,
    "MAILING_ADDRESS_LINE_2" TEXT,
    "MAILING_CITY" TEXT,
    "MAILING_STATE" TEXT,
    "MAILING_ZIP" TEXT,
    "MAILING_ZIP6" TEXT,
    "OFFICE_STOP_MAIL_FLAG" TEXT,
    "OFFICE_PHONE_NUMBER" TEXT,
    "ADDITIONAL_PHONE_NUMBER" TEXT,
    "OFFICE_FAX_NUMBER" TEXT,
    "OFFICE_STOP_FAX_FLAG" TEXT,
    "OFFICE_EMAIL_ADDRESS" TEXT,
    "NM_SALESPERSON_COUNT" INTEGER,
    "OFFICE_CONTACT_DR_ID" BIGINT,
    "OFFICE_CONTACT_MANAGER_ID" BIGINT,
    "OFFICE_CONTACT_UNLICENSED" TEXT,
    "DISTRICT" TEXT,
    "OFFICE_TYPE_DESCRIPTION" TEXT,
    "TAX_ID_NUMBER" TEXT,
    "CORPORATE_LICENSE_NUMBER" TEXT,
    "OFFICE_CORPORATE_NAME" TEXT,
    "OFFICE_FORMAL_NAME" TEXT,
    "MAIN_OFFICE_ID" BIGINT,
    "FRANCHISE_OFFICE_ID" BIGINT,
    "PARENT_COMPANY_OFFICE_ID" BIGINT,
    "BILLING_OFFICE_ID" BIGINT,
    "BRANCH_TYPE_CODE" TEXT,
    "OFFICE_PRIMARY_INDICATOR" TEXT,
    "MLS_ONLINE_STATUS" TEXT,
    "MLS_ONLINE_STATUS_DATE" DATE,
    "WEB_PAGE_ADDRESS" TEXT,
    "REGIONAL_MLS_ID" TEXT,
    "DIRECT_MARKETING_MAIL_FLAG" TEXT,
    "LAST_CHANGED_BY" TEXT,
    "LAST_CHANGED_DATETIME" TIMESTAMP
);

-- Add indexes to optimize queries
CREATE INDEX "idx_officeextract_office_id" ON "OfficeExtract" ("OFFICE_ID");
CREATE INDEX "idx_officeextract_local_association" ON "OfficeExtract" ("PRIMARY_LOCAL_ASSOCIATION_ID");
CREATE INDEX "idx_officeextract_state_association" ON "OfficeExtract" ("PRIMARY_STATE_ASSOCIATION_ID");
CREATE INDEX "idx_officeextract_status_code" ON "OfficeExtract" ("OFFICE_STATUS_CODE");
CREATE INDEX "idx_officeextract_city_state" ON "OfficeExtract" ("STREET_CITY", "STREET_STATE");
CREATE INDEX "idx_officeextract_billing_office_id" ON "OfficeExtract" ("BILLING_OFFICE_ID");

-- Create the BankMetadata table with BankID as the primary key
CREATE TABLE "BankMetadata" (
    "BankID" INT PRIMARY KEY,
    "AssociationCode" TEXT,
    "AssociationName" TEXT,
    "BankName" TEXT
);

-- Update the Invoicing table to reference BankID
CREATE TABLE "Invoicing" (
    "InvoiceID" SERIAL PRIMARY KEY,
    "BankID" INT REFERENCES "BankMetadata" ("BankID"),
    "DestinationAssociation" TEXT,
    "ACHSettlementNumber" TEXT,
    "ECControlNumber" TEXT,
    "MemberName" TEXT,
    "MemberID" BIGINT,
    "BillingYear" INT,
    "GrossAmount" NUMERIC,
    "AssociationPortion" NUMERIC,
    "TransactionFee" NUMERIC,
    "NetAssociationPortion" NUMERIC
);

-- Update the ManualEFT table to reference BankID
CREATE TABLE "ManualEFT" (
    "EFTID" SERIAL PRIMARY KEY,
    "BankID" INT REFERENCES "BankMetadata" ("BankID"),
    "ReceivingAssociation" TEXT,
    "ACHSettlementNumber" TEXT,
    "ECControlNumber" TEXT,
    "DestinationOrganization" TEXT,
    "Amount" NUMERIC
);
-- Create the ExternalInterface table
CREATE TABLE "ExternalInterface" (
    "BankID" INT, -- New column to store the BankID
    "DestinationAssociation" TEXT,
    "ACHSettlementNumber" TEXT,
    "ECControlNumber" TEXT,
    "MemberName" TEXT,
    "MemberID" BIGINT,
    "BillingYear" INT,
    "GrossAmountOfInvoice" NUMERIC,
    "AssociationPortionOfAmount" NUMERIC,
    "TransactionFeeOnAssocPortion" NUMERIC,
    "NetAssociationPortion" NUMERIC,
    "AccountName" TEXT,
    CONSTRAINT fk_externalinterface_bankid FOREIGN KEY ("BankID")
    REFERENCES "BankMetadata" ("BankID") -- Foreign key relationship to BankMetadata
);

-- Add indexes for faster queries
CREATE INDEX "idx_externalinterface_bankid" ON "ExternalInterface" ("BankID");
CREATE INDEX "idx_externalinterface_member_id" ON "ExternalInterface" ("MemberID");
CREATE INDEX "idx_externalinterface_billing_year" ON "ExternalInterface" ("BillingYear");
CREATE INDEX "idx_externalinterface_ec_control_number" ON "ExternalInterface" ("ECControlNumber");
-- Update the Chargeback table to reference BankID
CREATE TABLE "Chargeback" (
    "ChargebackID" SERIAL PRIMARY KEY,
    "BankID" INT REFERENCES "BankMetadata" ("BankID"),
    "ECControlNumber" TEXT,
    "TransactionNumber" TEXT,
    "DestinationOrganization" TEXT,
    "Amount" NUMERIC
);
