package in.novopay.creditcard.loc.util;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import in.novopay.infra.hdfc.api.loanoncard.constants.LoanOnCardConst;
import in.novopay.creditcard.constants.TransactionAuditConstants;
import in.novopay.creditcard.dao.TransactionAuditAttributesDAOService;
import in.novopay.infra.platform.navigation.DefaultExecutionContext;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class LocMisDeviceDetailsPersisterTest {

	private static final String CHROME = "Chrome";
	private static final String VER_120 = "120";
	private static final String WINDOWS = "Windows";
	private static final String OS_VER_10 = "10";
	private static final String LAT_LONG = "12.9,77.6";
	private static final String DSE_IP = "203.0.113.10";

	@Mock
	private LOCUtils locUtils;
	@Mock
	private TransactionAuditAttributesDAOService transactionAuditAttributesDAOService;

	@InjectMocks
	private LocMisDeviceDetailsPersister persister;

	@Test
	@DisplayName("PWA: persists full DSE browser pack + link channel")
	void persistDse_pwa_fullPack() {
		when(transactionAuditAttributesDAOService.findByTransactionAuditIdAndAttrKey(anyLong(), anyString()))
				.thenReturn(null);

		DefaultExecutionContext ctx = new DefaultExecutionContext();
		ctx.put(TransactionAuditConstants.CHANNEL_CODE, "WEB");
		ctx.put("client_ip", DSE_IP);
		Map<String, Object> browser = new HashMap<>();
		browser.put(LoanOnCardConst.BROWSER_NAME, CHROME);
		browser.put(LoanOnCardConst.BROWSER_VERSION, VER_120);
		browser.put(LoanOnCardConst.SYSTEM_OS, WINDOWS);
		browser.put(LoanOnCardConst.SYSTEM_OS_VERSION, OS_VER_10);
		browser.put(LoanOnCardConst.SYSTEM_LOCATION, LAT_LONG);
		ctx.put(LoanOnCardConst.BROWSER_DETAILS, browser);

		persister.persistDseDetailsFromExecutionContext(55L, ctx);

		verify(locUtils).createOrUpdateAttribute(55L, LoanOnCardConst.ATTR_DSE_LINK_CHANNEL, "PWA");
		verify(locUtils).createOrUpdateAttribute(55L, LoanOnCardConst.ATTR_DSE_BROWSER_NAME, CHROME);
		verify(locUtils).createOrUpdateAttribute(55L, LoanOnCardConst.ATTR_DSE_BROWSER_VERSION, VER_120);
		verify(locUtils).createOrUpdateAttribute(55L, LoanOnCardConst.ATTR_DSE_SYSTEM_OS, WINDOWS);
		verify(locUtils).createOrUpdateAttribute(55L, LoanOnCardConst.ATTR_DSE_SYSTEM_OS_VERSION, OS_VER_10);
		verify(locUtils).createOrUpdateAttribute(55L, LoanOnCardConst.ATTR_DSE_SYSTEM_LOCATION, LAT_LONG);
		verify(locUtils).createOrUpdateAttribute(55L, LoanOnCardConst.ATTR_DSE_SYSTEM_IP_ADDRESS, DSE_IP);
	}

	@Test
	@DisplayName("APK: skips browser name/version; keeps OS/location/IP")
	void persistDse_apk_skipsBrowser() {
		when(transactionAuditAttributesDAOService.findByTransactionAuditIdAndAttrKey(anyLong(), anyString()))
				.thenReturn(null);

		DefaultExecutionContext ctx = new DefaultExecutionContext();
		ctx.put(TransactionAuditConstants.CHANNEL_CODE, "APP");
		ctx.put("client_ip", DSE_IP);
		Map<String, Object> browser = new HashMap<>();
		browser.put(LoanOnCardConst.BROWSER_NAME, CHROME);
		browser.put(LoanOnCardConst.BROWSER_VERSION, VER_120);
		browser.put(LoanOnCardConst.SYSTEM_OS, "Android");
		browser.put(LoanOnCardConst.SYSTEM_OS_VERSION, "14");
		browser.put(LoanOnCardConst.SYSTEM_LOCATION, LAT_LONG);
		ctx.put(LoanOnCardConst.BROWSER_DETAILS, browser);

		persister.persistDseDetailsFromExecutionContext(66L, ctx);

		verify(locUtils).createOrUpdateAttribute(66L, LoanOnCardConst.ATTR_DSE_LINK_CHANNEL, "APK");
		verify(locUtils, never())
				.createOrUpdateAttribute(eq(66L), eq(LoanOnCardConst.ATTR_DSE_BROWSER_NAME), anyString());
		verify(locUtils, never())
				.createOrUpdateAttribute(eq(66L), eq(LoanOnCardConst.ATTR_DSE_BROWSER_VERSION), anyString());
		verify(locUtils).createOrUpdateAttribute(66L, LoanOnCardConst.ATTR_DSE_SYSTEM_OS, "Android");
		verify(locUtils).createOrUpdateAttribute(66L, LoanOnCardConst.ATTR_DSE_SYSTEM_LOCATION, LAT_LONG);
	}

	@Test
	@DisplayName("resolveDseLinkChannel maps WEB/APP")
	void resolveChannel() {
		assertThat(LocMisDeviceDetailsPersister.resolveDseLinkChannel("WEB")).isEqualTo("PWA");
		assertThat(LocMisDeviceDetailsPersister.resolveDseLinkChannel("APP")).isEqualTo("APK");
		assertThat(LocMisDeviceDetailsPersister.resolveDseLinkChannel(" ")).isEmpty();
	}
}
