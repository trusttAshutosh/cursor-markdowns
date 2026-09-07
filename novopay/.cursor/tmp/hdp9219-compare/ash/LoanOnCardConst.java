package in.novopay.infra.hdfc.api.loanoncard.constants;

public class LoanOnCardConst {

    //Preferred SOAP prefix
    public static final String SOAPENV = "soapenv";

    //NameSpaces
    public static final String TRAN = "tran";
    public static final String INQ = "inq";
    public static final String CON = "con";
    public static final String EXC = "exc";
    public static final String DAT = "dat";
    public static final String DTO = "dto";
    public static final String DOM = "dom";

    //Namespaces mapping
    public static final String TRAN_NAMESPACE = "http://transaction.service.cards.appx.cz.fc.ofss.com/";
    public static final String INQ_NAMESPACE = "http://inquiry.service.cards.appx.cz.fc.ofss.com/";
    public static final String CON_NAMESPACE = "http://context.app.fc.ofss.com";
    public static final String EXC_NAMESPACE = "http://exception.infra.fc.ofss.com";
    public static final String DAT_NAMESPACE = "http://datatype.fc.ofss.com";
    public static final String RESPONSE_NAMESPACE = "http://response.service.fc.ofss.com";
    public static final String DTO_NAMESPACE = "http://dto.common.domain.framework.fc.ofss.com";
    public static final String DOM_NAMESPACE = "http://domain.framework.fc.ofss.com";

    //API Value Constants
    public static final String MOBILE_NO = "mobile_no";
    public static final String CARD_NO = "card_no";
    public static final String AAN = "aan";
    public static final String MOB_NBR = "MOB_NBR";
    public static final String SVC_RETURN = "svc_return";
    public static final String AVAILABLE_CREDIT_LIMIT = "available_credit_limit";
    public static final String CARD_HOLDER_NAME = "card_holder_name";
    public static final String ACCOUNT_NUMBER = "account_number";
    public static final String LOAN_NUMBER = "loan_number";
    public static final String RELATION_NUMBER = "relation_number";
    public static final String FULL_NAME = "full_name";
    public static final String TID = "tid";
    public static final String EMAIL = "email";
    public static final String KFS_DOCUMENT_REF_NUMBER = "reference_number";
    public static final String LOAN_PURPOSE_CODE = "loan_purpose_code";
    public static final String KFS_DOCUMENT_LANGUAGE = "kfs_document_language";
    public static final String EXTERNAL_REFERENCE_NUMBER = "external_reference_number";
    public static final String LANGUAGE_CODE = "language_code";

    /** HDFC bank Error code, stamped by LOC adapters before throwing. */
    public static final String LOC_BANK_ERROR_CODE = "loc_bank_error_code";
    /** HDFC Error scenario (bank reply text), stamped by LOC adapters. */
    public static final String LOC_BANK_ERROR_SCENARIO = "loc_bank_error_scenario";
    public static final String SRVC_ERROR_CODE = "srvc_error_code";
    public static final String SRVC_ERROR_DESC = "srvc_error_desc";
    public static final String DESCRIPTION_OF_ERROR_MSG = "description_of_error_msg";

    /** Execution-context key for stamped HDFC bank API name (audit / logs). */
    public static final String BANK_API_NAME = "bank_api_name";
    public static final String TXN_RESPONSE_CODE = "txn_response_code";
    public static final String TXN_RESPONSE_DESCRIPTION = "txn_response_description";

    public static final String GET_CARD_SUMMARY = "getCardSummary";
    public static final String INQUIRE_CARD_DETAILS = "inquireCardDetails";
    public static final String INQUIRE_CREDIT_CARD_PRODUCT_ELIGIBILITY = "inquireCreditCardProductEligibility";
    public static final String SUBMIT_INSTA_LOAN = "submitInstaLoan";
    public static final String SUBMIT_INSTA_JUMBO_LOAN = "submitInstaJumboLoan";

    public static final String INSTA_PRODUCT_CODE = "007";
    public static final String JUMBO_PRODUCT_CODE = "010";

    public static final String SERVICE_INSTA_BOOKING = "BBICOC";
    public static final String SERVICE_JUMBO_BOOKING = "BBIPLC";

    public static final String ADDRESS_1 = "address1";
    public static final String ADDRESS_2 = "address2";
    public static final String ADDRESS_3 = "address3";
    public static final String ADDRESS_5 = "address5";
    public static final String ADDRESS_4 = "address4";
    public static final String CITY = "city";
    public static final String STATE = "state";
    public static final String POSTAL_CODE = "postalCode";

    public static final String BLOCK_CODE_1 = "blockCode1";
    public static final String BLOCK_CODE_2 = "blockCode2";
    public static final String LOGO = "Logo";
    public static final String LOGO_DESCRIPTION = "logoDescription";

    public static final String CUSTOMER_ADDRESS = "customer_address";

    public static final String RECIPIENT_COUNT = "recipient_count";
    public static final String RECIPIENT_NAME = "recipient_name";
    public static final String ACCOUNT_CARD_TYPE = "account_card_type";

    public static final String PRIMARY_CARD_TYPE = "P";
    public static final String ADD_ON_CARD_TYPE = "A";

    public static final String LOC_TRANSACTION_SUB_TYPE = "LOC";

    /** No eligible LOC products (empty eligibility list). */
    public static final String LOC_NO_PRODUCTS_ERROR_CODE = "4000359";
    /** Customer-facing no-offers copy (notifications DDP-364; codes 4000359 and 4000373). */
    public static final String LOC_NO_PRODUCTS_DESC =
            "Customer not eligible! Unfortunately, the customer is not eligible for any of the loans on their Credit Card.";
    public static final String MOBILE_NOT_ELIGIBLE_CODE = "4000358";
    public static final String NO_CASA_ACCOUNT_CODE = "4000297";
    public static final String NO_CASA_ACCOUNT_DESC =
            "The customer does not have a Current or Savings Account.";

    public static final String INSTA_INVALID_ACCOUNT = "4000346";
    public static final String INSTA_ACCOUNT_BLOCKED = "4000347";
    public static final String INSTA_RETRY_AFTER_48H = "4000348";
    public static final String INSTA_RETRY_LATER = "4000349";
    public static final String INSTA_INCORRECT_ACCOUNT = "4000350";
    public static final String JUMBO_INCORRECT_ACCOUNT = "4000351";
    public static final String JUMBO_INVALID_ACCOUNT = "4000352";
    public static final String JUMBO_ACCOUNT_BLOCKED = "4000353";
    public static final String ADD_ON_CARD = "4000354";
    public static final String AMOUNT_EXCEEDS_LIMIT_OR_ALREADY_AVAILED = "4000355";
    public static final String AMOUNT_EXCEEDS_RETRY_LOWER = "4000356";
    public static final String TECHNICAL_ISSUE = "4000357";
    public static final String INSTA_AMOUNT_EXCEEDS_OTB = "4000371";
    public static final String JUMBO_PRODUCT_ELIG_NOT_FOUND = "4000372";

    /** HDFC bank error when TID / tenure list is missing on eligibility response. */
    public static final String BANK_ERROR_MISSING_TID = "159";

    /** Persisted on successful getLOCOffers when insta (007) is in the filtered product list (DSA count table). */
    public static final String LOC_INSTA_OFFER_AVAILABLE = "loc_insta_offer_available";
    /** Persisted on successful getLOCOffers when jumbo (010) is in the filtered product list (DSA count table). */
    public static final String LOC_JUMBO_OFFER_AVAILABLE = "loc_jumbo_offer_available";
    public static final String LOC_OFFER_AVAILABLE_VALUE = "Y";
    public static final String LOC_OFFER_UNAVAILABLE_VALUE = "N";

    /** Execution-context flag: income-based jumbo dummy eligibility is active (jumbo treated as not offered). */
    public static final String LOC_JUMBO_DUMMY_ELIGIBILITY_ACTIVE = "loc_jumbo_dummy_eligibility_active";
    public static final String LOC_JUMBO_DUMMY_ELIGIBILITY_ACTIVE_VALUE = "Y";

    /** Parsed LCM Offer Inquiry pseudoId used to suppress jumbo when present. */
    public static final String LOC_JUMBO_LCM_PSEUDO_ID = "loc_jumbo_lcm_pseudo_id";

    /** Jumbo suppression cause labels for structured ops logs. */
    public static final String LOC_JUMBO_RESTRICTION_CAUSE_PE_PQ = "PE-PQ";
    public static final String LOC_JUMBO_RESTRICTION_CAUSE_LCM_PSEUDO_ID = "LCM pseudoId";

    /** Where the bank signal was read (API + field path). */
    public static final String LOC_JUMBO_RESTRICTION_LOCATION_PE_PQ =
            "inquireCreditCardProductEligibility/HIBVPRD product 010 MEMO-LINE2 (block offsets 125-165)";
    public static final String LOC_JUMBO_RESTRICTION_LOCATION_LCM_PSEUDO_ID =
            "locOfferInquiryOfInstaJumboLoan/offerInquiryList[].conventionalOfferDTO.pseudoId";

    /** Customer-facing error when no jumbo offer is available due to PE-PQ dummy eligibility. */
    public static final String LOC_JUMBO_DUMMY_ELIGIBILITY_CODE = "4000373";
    public static final String LOC_JUMBO_DUMMY_ELIGIBILITY_MSG = LOC_NO_PRODUCTS_DESC;

    /** HDP-9219: request map / flat EC keys for DSE browser_details on manageLOC. */
    public static final String BROWSER_DETAILS = "browser_details";
    public static final String BROWSER_NAME = "browser_name";
    public static final String BROWSER_VERSION = "browser_version";
    public static final String SYSTEM_OS = "system_os";
    public static final String SYSTEM_OS_VERSION = "system_os_version";
    public static final String SYSTEM_IP_ADDRESS = "system_ip_address";
    public static final String SYSTEM_LOCATION = "system_location";

    /** HDP-9219: DSE link-trigger channel values for MIS (channel_code WEB→PWA, APP→APK). */
    public static final String ATTR_DSE_LINK_CHANNEL = "dse_link_channel";
    public static final String DSE_LINK_CHANNEL_PWA = "PWA";
    public static final String DSE_LINK_CHANNEL_APK = "APK";

    public static final String ATTR_DSE_BROWSER_NAME = "dse_browser_name";
    public static final String ATTR_DSE_BROWSER_VERSION = "dse_browser_version";
    public static final String ATTR_DSE_SYSTEM_LOCATION = "dse_system_location";
    public static final String ATTR_DSE_SYSTEM_OS_VERSION = "dse_system_os_version";
    public static final String ATTR_DSE_SYSTEM_IP_ADDRESS = "dse_system_ip_address";
    public static final String ATTR_DSE_SYSTEM_OS = "dse_system_os";

    public static final String ATTR_CUSTOMER_BROWSER_NAME = "customer_browser_name";
    public static final String ATTR_CUSTOMER_BROWSER_VERSION = "customer_browser_version";
    public static final String ATTR_CUSTOMER_SYSTEM_LOCATION = "customer_system_location";
    public static final String ATTR_CUSTOMER_SYSTEM_OS_VERSION = "customer_system_os_version";
    public static final String ATTR_CUSTOMER_SYSTEM_IP_ADDRESS = "customer_system_ip_address";
    public static final String ATTR_CUSTOMER_SYSTEM_OS = "customer_system_os";

    public static final String CONSENT_BROWSER_NAME = "consent_browser_name";
    public static final String CONSENT_BROWSER_VERSION = "consent_browser_version";
    public static final String CONSENT_SYSTEM_OS = "consent_system_os";
    public static final String CONSENT_SYSTEM_OS_VERSION = "consent_system_os_version";
    public static final String CONSENT_SYSTEM_IP_ADDRESS = "consent_system_ip_address";
    public static final String CONSENT_SYSTEM_LOCATION = "consent_system_location";

    private LoanOnCardConst() {
    }
}
