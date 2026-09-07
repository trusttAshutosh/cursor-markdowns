package in.novopay.creditcard.loc.util;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import in.novopay.creditcard.constants.LocMisAttrKeys;
import in.novopay.creditcard.dao.TransactionAuditAttributesDAOService;
import in.novopay.infra.platform.navigation.DefaultExecutionContext;
import in.novopay.infra.platform.navigation.ExecutionContext;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** HDP-9219: agent capture is header-only, customer capture is browser_details-only. */
class LocMisDeviceDetailsPersisterTest {

    private static final long TXN_ID = 84321L;
    private static final String KEY_CHANNEL_CODE = "channel_code";
    private static final String AGENT_IP = "172.16.5.10";
    private static final String AGENT_LOCATION = "12.918524,77.670120";
    private static final String BROWSER_CHROME = "Chrome";
    private static final String BROWSER_CHROME_VERSION = "151.0.0.0";
    private static final String OS_WINDOWS = "Windows";
    private static final String CHROME_WIN =
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                    + " Chrome/151.0.0.0 Safari/537.36";

    private LOCUtils locUtils;
    private TransactionAuditAttributesDAOService attrDao;
    private LocMisDeviceDetailsPersister persister;

    @BeforeEach
    void setUp() {
        locUtils = mock(LOCUtils.class);
        attrDao = mock(TransactionAuditAttributesDAOService.class);
        when(attrDao.findByTransactionAuditIdAndAttrKey(anyLong(), anyString())).thenReturn(null);
        persister = new LocMisDeviceDetailsPersister(locUtils, attrDao);
    }

    private static ExecutionContext agentContext(String channelCode) {
        ExecutionContext ctx = new DefaultExecutionContext();
        ctx.put(KEY_CHANNEL_CODE, channelCode);
        ctx.put(LocMisAttrKeys.EC_KEY_HTTP_USER_AGENT, CHROME_WIN);
        ctx.put("location", AGENT_LOCATION);
        ctx.put("client_ip", AGENT_IP);
        return ctx;
    }

    private static Map<String, Object> customerBrowserDetails() {
        Map<String, Object> details = new HashMap<>();
        details.put(LocMisAttrKeys.BROWSER_NAME, BROWSER_CHROME);
        details.put(LocMisAttrKeys.BROWSER_VERSION, BROWSER_CHROME_VERSION);
        details.put(LocMisAttrKeys.SYSTEM_OS, OS_WINDOWS);
        details.put(LocMisAttrKeys.SYSTEM_OS_VERSION, "10");
        details.put(LocMisAttrKeys.SYSTEM_LOCATION, "12.971598,77.594566");
        return details;
    }

    /* ---------------- agent ---------------- */

    @Test
    @DisplayName("PWA: writes the full agent pack including browser name and version")
    void pwaWritesFullPack() {
        persister.persistAgentDetails(TXN_ID, agentContext("WEB"));

        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_LINK_CHANNEL, "PWA");
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_BROWSER_NAME, BROWSER_CHROME);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_BROWSER_VERSION, BROWSER_CHROME_VERSION);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_SYSTEM_OS, OS_WINDOWS);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_SYSTEM_OS_VERSION, "10");
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_SYSTEM_LOCATION, AGENT_LOCATION);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_SYSTEM_IP_ADDRESS, AGENT_IP);
    }

    @Test
    @DisplayName("APK: skips browser name and version, keeps OS, location and IP")
    void apkSkipsBrowserFields() {
        persister.persistAgentDetails(TXN_ID, agentContext("APP"));

        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_LINK_CHANNEL, "APK");
        verify(locUtils, never()).createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_BROWSER_NAME), anyString());
        verify(locUtils, never())
                .createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_BROWSER_VERSION), anyString());
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_SYSTEM_OS, OS_WINDOWS);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_SYSTEM_IP_ADDRESS, AGENT_IP);
    }

    @Test
    @DisplayName("agent path never reads browser_details, so customer values cannot land in dse_* keys")
    void agentPathIgnoresBrowserDetails() {
        ExecutionContext ctx = agentContext("WEB");
        Map<String, Object> customerDetails = new HashMap<>();
        customerDetails.put(LocMisAttrKeys.BROWSER_NAME, "CustomerBrowser");
        customerDetails.put(LocMisAttrKeys.SYSTEM_OS, "CustomerOS");
        customerDetails.put(LocMisAttrKeys.SYSTEM_LOCATION, "99.999999,99.999999");
        ctx.put(LocMisAttrKeys.BROWSER_DETAILS, customerDetails);

        persister.persistAgentDetails(TXN_ID, ctx);

        verify(locUtils, never())
                .createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_BROWSER_NAME), eq("CustomerBrowser"));
        verify(locUtils, never())
                .createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_SYSTEM_OS), eq("CustomerOS"));
        verify(locUtils, never())
                .createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_SYSTEM_LOCATION), eq("99.999999,99.999999"));
        // header-derived values still win
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_BROWSER_NAME, BROWSER_CHROME);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_SYSTEM_LOCATION, AGENT_LOCATION);
    }

    @Test
    @DisplayName("blank location and loopback-only client_ip write nothing for those keys")
    void blankAndLoopbackInputsSkipped() {
        ExecutionContext ctx = new DefaultExecutionContext();
        ctx.put(KEY_CHANNEL_CODE, "WEB");
        ctx.put(LocMisAttrKeys.EC_KEY_HTTP_USER_AGENT, CHROME_WIN);
        ctx.put("client_ip", "127.0.0.1");

        persister.persistAgentDetails(TXN_ID, ctx);

        verify(locUtils, never())
                .createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_SYSTEM_LOCATION), anyString());
        verify(locUtils, never())
                .createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_SYSTEM_IP_ADDRESS), anyString());
    }

    @Test
    @DisplayName("location of NA is treated as blank and never stored")
    void naLocationRejected() {
        ExecutionContext ctx = agentContext("WEB");
        ctx.put("location", "NA");

        persister.persistAgentDetails(TXN_ID, ctx);

        verify(locUtils, never())
                .createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_SYSTEM_LOCATION), anyString());
    }

    @Test
    @DisplayName("first write wins: an existing attribute is never overwritten")
    void existingAttributeNotOverwritten() {
        when(attrDao.findByTransactionAuditIdAndAttrKey(TXN_ID, LocMisAttrKeys.DSE_BROWSER_NAME))
                .thenReturn("Firefox");

        persister.persistAgentDetails(TXN_ID, agentContext("WEB"));

        verify(locUtils, never()).createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_BROWSER_NAME), anyString());
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.DSE_BROWSER_VERSION, BROWSER_CHROME_VERSION);
    }

    @Test
    @DisplayName("non-positive audit id is a no-op")
    void nonPositiveAuditIdIgnored() {
        persister.persistAgentDetails(0L, agentContext("WEB"));

        verify(locUtils, never()).createOrUpdateAttribute(anyLong(), anyString(), anyString());
    }

    /* ---------------- customer ---------------- */

    @Test
    @DisplayName("customer: writes the five browser_details fields")
    void customerWritesFiveFields() {
        ExecutionContext ctx = new DefaultExecutionContext();
        ctx.put(LocMisAttrKeys.BROWSER_DETAILS, customerBrowserDetails());

        persister.persistCustomerDetails(TXN_ID, ctx);

        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.CUSTOMER_BROWSER_NAME, BROWSER_CHROME);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.CUSTOMER_BROWSER_VERSION, BROWSER_CHROME_VERSION);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.CUSTOMER_SYSTEM_OS, OS_WINDOWS);
        verify(locUtils).createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.CUSTOMER_SYSTEM_OS_VERSION, "10");
        verify(locUtils)
                .createOrUpdateAttribute(TXN_ID, LocMisAttrKeys.CUSTOMER_SYSTEM_LOCATION, "12.971598,77.594566");
    }

    @Test
    @DisplayName("customer: IP is never taken from the FE payload")
    void customerIpNeverFromRequest() {
        Map<String, Object> details = customerBrowserDetails();
        details.put("system_ip_address", "49.37.212.44");
        ExecutionContext ctx = new DefaultExecutionContext();
        ctx.put(LocMisAttrKeys.BROWSER_DETAILS, details);

        persister.persistCustomerDetails(TXN_ID, ctx);

        verify(locUtils, never())
                .createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.CUSTOMER_SYSTEM_IP_ADDRESS), anyString());
    }

    @Test
    @DisplayName("customer: absent browser_details writes nothing")
    void customerWithoutBrowserDetails() {
        persister.persistCustomerDetails(TXN_ID, new DefaultExecutionContext());

        verify(locUtils, never()).createOrUpdateAttribute(anyLong(), anyString(), anyString());
    }

    @Test
    @DisplayName("customer path writes no dse_* key")
    void customerPathWritesNoAgentKey() {
        ExecutionContext ctx = new DefaultExecutionContext();
        ctx.put(LocMisAttrKeys.BROWSER_DETAILS, customerBrowserDetails());
        ctx.put(KEY_CHANNEL_CODE, "WEB");
        ctx.put(LocMisAttrKeys.EC_KEY_HTTP_USER_AGENT, CHROME_WIN);

        persister.persistCustomerDetails(TXN_ID, ctx);

        verify(locUtils, never()).createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_LINK_CHANNEL), anyString());
        verify(locUtils, never()).createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_BROWSER_NAME), anyString());
        verify(locUtils, never()).createOrUpdateAttribute(anyLong(), eq(LocMisAttrKeys.DSE_SYSTEM_OS), anyString());
    }

    /* ---------------- link channel ---------------- */

    @Test
    @DisplayName("resolveLinkChannel maps WEB and APP, passes others through, blanks stay blank")
    void resolveLinkChannelMapping() {
        assertThat(LocMisDeviceDetailsPersister.resolveLinkChannel("WEB")).isEqualTo("PWA");
        assertThat(LocMisDeviceDetailsPersister.resolveLinkChannel("web")).isEqualTo("PWA");
        assertThat(LocMisDeviceDetailsPersister.resolveLinkChannel("APP")).isEqualTo("APK");
        assertThat(LocMisDeviceDetailsPersister.resolveLinkChannel(" ")).isEmpty();
        assertThat(LocMisDeviceDetailsPersister.resolveLinkChannel(null)).isEmpty();
        assertThat(LocMisDeviceDetailsPersister.resolveLinkChannel("kiosk")).isEqualTo("KIOSK");
    }
}
