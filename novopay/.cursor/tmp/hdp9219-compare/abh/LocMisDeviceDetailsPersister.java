package in.novopay.creditcard.loc.util;

import in.novopay.creditcard.common.device.UserAgentParser;
import in.novopay.creditcard.common.ip.GatewayUsableClientIp;
import in.novopay.creditcard.constants.LocMisAttrKeys;
import in.novopay.creditcard.constants.TransactionAuditConstants;
import in.novopay.creditcard.dao.TransactionAuditAttributesDAOService;
import in.novopay.infra.platform.navigation.ExecutionContext;
import java.util.Map;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/**
 * HDP-9219: persists the LOC MIS device-detail attributes onto {@code transaction_audit_attributes}.
 *
 * <p>Two strictly separate sources, one party each:
 * <ul>
 *   <li><b>Agent</b> — {@link #persistAgentDetails} reads the gateway headers of the request itself
 *       ({@code httpheader_user-agent}, {@code client_ip}, {@code location}). It never reads
 *       {@code browser_details}.</li>
 *   <li><b>Customer</b> — {@link #persistCustomerDetails} reads only the request's
 *       {@code browser_details} map, relayed by the FE from {@code getCustomerConsentStatus}.</li>
 * </ul>
 *
 * <p>Keeping the agent path header-only is what prevents customer {@code browser_details} sent on
 * {@code getLOCOffers} from ever landing in {@code dse_*} keys.
 *
 * <p>All writes are first-write-wins: a populated attribute is never overwritten.
 */
@Service
public class LocMisDeviceDetailsPersister {

    private static final Logger LOG = LoggerFactory.getLogger(LocMisDeviceDetailsPersister.class);

    /** The consent portal sends this when geolocation is denied; it must never be stored. */
    private static final String NOT_AVAILABLE = "NA";

    private final LOCUtils locUtils;
    private final TransactionAuditAttributesDAOService attrDao;

    public LocMisDeviceDetailsPersister(LOCUtils locUtils, TransactionAuditAttributesDAOService attrDao) {
        this.locUtils = locUtils;
        this.attrDao = attrDao;
    }

    /**
     * Agent (DSE) device details, from this request's own gateway headers. Browser name and version are
     * skipped on APK, which has no browser (HDP-9219 rule 2).
     */
    public void persistAgentDetails(long txnAuditId, ExecutionContext ctx) {
        if (txnAuditId <= 0 || ctx == null) {
            return;
        }
        String linkChannel = resolveLinkChannel(ctx.getStringValue(TransactionAuditConstants.CHANNEL_CODE));
        putAttrIfBlank(txnAuditId, LocMisAttrKeys.DSE_LINK_CHANNEL, linkChannel);

        String userAgent = ctx.getStringValue(LocMisAttrKeys.EC_KEY_HTTP_USER_AGENT);
        UserAgentParser.DeviceInfo device = UserAgentParser.parse(userAgent);

        if (!LocMisAttrKeys.LINK_CHANNEL_APK.equals(linkChannel)) {
            putAttrIfBlank(txnAuditId, LocMisAttrKeys.DSE_BROWSER_NAME, device.browserName());
            putAttrIfBlank(txnAuditId, LocMisAttrKeys.DSE_BROWSER_VERSION, device.browserVersion());
        }
        putAttrIfBlank(txnAuditId, LocMisAttrKeys.DSE_SYSTEM_OS, device.osName());
        putAttrIfBlank(txnAuditId, LocMisAttrKeys.DSE_SYSTEM_OS_VERSION, device.osVersion());
        putAttrIfBlank(
                txnAuditId,
                LocMisAttrKeys.DSE_SYSTEM_LOCATION,
                ctx.getStringValue(TransactionAuditConstants.LOCATION));

        // Gateway-resolved only: the FE is never trusted to report its own IP.
        String agentIp =
                GatewayUsableClientIp.firstUsableFromGatewayPick(ctx.getStringValue(LocMisAttrKeys.EC_KEY_CLIENT_IP));
        putAttrIfBlank(txnAuditId, LocMisAttrKeys.DSE_SYSTEM_IP_ADDRESS, agentIp);

        LOG.info(
                "LOC_MIS_AGENT_DEVICE_PERSIST txn_id={} link_channel={} ua_present={} browser_parsed={}",
                txnAuditId,
                linkChannel,
                StringUtils.isNotBlank(userAgent),
                StringUtils.isNotBlank(device.browserName()));
    }

    /**
     * Customer device details, from the request's {@code browser_details} map. The customer IP is
     * intentionally not taken from here — it stays server-sourced so it is never self-reported through
     * the agent's app.
     */
    public void persistCustomerDetails(long txnAuditId, ExecutionContext ctx) {
        if (txnAuditId <= 0 || ctx == null) {
            return;
        }
        Map<String, Object> details = resolveBrowserDetails(ctx);

        putAttrIfBlank(txnAuditId, LocMisAttrKeys.CUSTOMER_BROWSER_NAME, mapVal(details, LocMisAttrKeys.BROWSER_NAME));
        putAttrIfBlank(
                txnAuditId, LocMisAttrKeys.CUSTOMER_BROWSER_VERSION, mapVal(details, LocMisAttrKeys.BROWSER_VERSION));
        putAttrIfBlank(txnAuditId, LocMisAttrKeys.CUSTOMER_SYSTEM_OS, mapVal(details, LocMisAttrKeys.SYSTEM_OS));
        putAttrIfBlank(
                txnAuditId,
                LocMisAttrKeys.CUSTOMER_SYSTEM_OS_VERSION,
                mapVal(details, LocMisAttrKeys.SYSTEM_OS_VERSION));
        putAttrIfBlank(
                txnAuditId, LocMisAttrKeys.CUSTOMER_SYSTEM_LOCATION, mapVal(details, LocMisAttrKeys.SYSTEM_LOCATION));

        LOG.info(
                "LOC_MIS_CUSTOMER_DEVICE_PERSIST txn_id={} has_browser_details={}",
                txnAuditId,
                !details.isEmpty());
    }

    /** {@code WEB} to {@code PWA}, {@code APP} to {@code APK}; blank stays blank. */
    static String resolveLinkChannel(String channelCode) {
        if (StringUtils.isBlank(channelCode)) {
            return "";
        }
        String trimmed = channelCode.trim();
        if ("APP".equalsIgnoreCase(trimmed)) {
            return LocMisAttrKeys.LINK_CHANNEL_APK;
        }
        if ("WEB".equalsIgnoreCase(trimmed)) {
            return LocMisAttrKeys.LINK_CHANNEL_PWA;
        }
        return trimmed.toUpperCase();
    }

    /**
     * The single write path. Skips blanks and {@code "NA"}, and never overwrites a populated attribute.
     */
    private void putAttrIfBlank(long txnAuditId, String attrKey, String value) {
        if (isNaOrBlank(value)) {
            return;
        }
        String existing = StringUtils.trimToEmpty(attrDao.findByTransactionAuditIdAndAttrKey(txnAuditId, attrKey));
        if (StringUtils.isNotBlank(existing)) {
            return;
        }
        locUtils.createOrUpdateAttribute(txnAuditId, attrKey, value.trim());
    }

    private static boolean isNaOrBlank(String value) {
        String trimmed = StringUtils.trimToEmpty(value);
        return trimmed.isEmpty() || NOT_AVAILABLE.equalsIgnoreCase(trimmed);
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> resolveBrowserDetails(ExecutionContext ctx) {
        Object raw = ctx.get(LocMisAttrKeys.BROWSER_DETAILS);
        if (raw instanceof Map<?, ?> map) {
            return (Map<String, Object>) map;
        }
        return Map.of();
    }

    private static String mapVal(Map<String, Object> details, String key) {
        if (details == null || details.isEmpty()) {
            return "";
        }
        Object value = details.get(key);
        return value == null ? "" : StringUtils.trimToEmpty(String.valueOf(value));
    }
}
