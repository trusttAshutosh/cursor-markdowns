package in.novopay.creditcard.constants;

/**
 * HDP-9219: {@code transaction_audit_attributes} keys for the LOC MIS device-detail columns, plus the
 * request-side field names used by the customer payload.
 *
 * <p>Deliberately defined in this repo rather than in {@code LoanOnCardConst}: the lib {@code ddp-prod}
 * line does not carry these constants, so keeping them local leaves this branch free of any cross-repo
 * release dependency. The values are fixed by the MIS contract and are not needed by any other service.
 */
public final class LocMisAttrKeys {

    /* ---------- agent (DSE) attribute keys ---------- */

    public static final String DSE_LINK_CHANNEL = "dse_link_channel";
    public static final String DSE_BROWSER_NAME = "dse_browser_name";
    public static final String DSE_BROWSER_VERSION = "dse_browser_version";
    public static final String DSE_SYSTEM_OS = "dse_system_os";
    public static final String DSE_SYSTEM_OS_VERSION = "dse_system_os_version";
    public static final String DSE_SYSTEM_LOCATION = "dse_system_location";
    public static final String DSE_SYSTEM_IP_ADDRESS = "dse_system_ip_address";

    /* ---------- customer attribute keys ---------- */

    public static final String CUSTOMER_BROWSER_NAME = "customer_browser_name";
    public static final String CUSTOMER_BROWSER_VERSION = "customer_browser_version";
    public static final String CUSTOMER_SYSTEM_OS = "customer_system_os";
    public static final String CUSTOMER_SYSTEM_OS_VERSION = "customer_system_os_version";
    public static final String CUSTOMER_SYSTEM_LOCATION = "customer_system_location";
    public static final String CUSTOMER_SYSTEM_IP_ADDRESS = "customer_system_ip_address";

    /* ---------- dse_link_channel values ---------- */

    /** {@code channel_code=WEB} — DSE triggered the customer link from the progressive web app. */
    public static final String LINK_CHANNEL_PWA = "PWA";

    /** {@code channel_code=APP} — DSE triggered the customer link from the mobile APK. */
    public static final String LINK_CHANNEL_APK = "APK";

    /* ---------- request / ExecutionContext field names (customer payload) ---------- */

    public static final String BROWSER_DETAILS = "browser_details";
    public static final String BROWSER_NAME = "browser_name";
    public static final String BROWSER_VERSION = "browser_version";
    public static final String SYSTEM_OS = "system_os";
    public static final String SYSTEM_OS_VERSION = "system_os_version";
    public static final String SYSTEM_LOCATION = "system_location";

    /* ---------- gateway header keys (agent payload) ---------- */

    public static final String EC_KEY_HTTP_USER_AGENT = "httpheader_user-agent";
    public static final String EC_KEY_CLIENT_IP = "client_ip";

    private LocMisAttrKeys() {
    }
}
