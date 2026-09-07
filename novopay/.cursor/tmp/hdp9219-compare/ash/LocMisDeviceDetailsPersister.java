package in.novopay.creditcard.loc.util;

import in.novopay.creditcard.common.ip.GatewayUsableClientIp;
import in.novopay.infra.hdfc.api.loanoncard.constants.LoanOnCardConst;
import in.novopay.creditcard.constants.TransactionAuditConstants;
import in.novopay.creditcard.dao.TransactionAuditAttributesDAOService;
import in.novopay.infra.platform.navigation.ExecutionContext;
import java.util.Map;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/**
 * HDP-9219: persist DSE (agent link-trigger) and Customer (consent portal) device details
 * onto {@code transaction_audit_attributes} for LOC MIS.
 */
@Service
public class LocMisDeviceDetailsPersister {

	private static final Logger LOG = LoggerFactory.getLogger(LocMisDeviceDetailsPersister.class);

	private final LOCUtils locUtils;
	private final TransactionAuditAttributesDAOService transactionAuditAttributesDAOService;

	public LocMisDeviceDetailsPersister(
			LOCUtils locUtils, TransactionAuditAttributesDAOService transactionAuditAttributesDAOService) {
		this.locUtils = locUtils;
		this.transactionAuditAttributesDAOService = transactionAuditAttributesDAOService;
	}

	/**
	 * Capture DSE device details from request {@code browser_details} (or flat EC keys) plus
	 * gateway agent IP / {@code channel_code}. PWA keeps browser name/version; APK skips them.
	 * First-write-wins per attribute.
	 */
	public void persistDseDetailsFromExecutionContext(long transactionAuditId, ExecutionContext executionContext) {
		if (transactionAuditId <= 0 || executionContext == null) {
			return;
		}
		String linkChannel = resolveDseLinkChannel(executionContext.getStringValue(TransactionAuditConstants.CHANNEL_CODE));
		putAttrIfBlank(transactionAuditId, LoanOnCardConst.ATTR_DSE_LINK_CHANNEL, linkChannel);

		Map<String, Object> details = resolveBrowserDetailsMap(executionContext);
		boolean apk = LoanOnCardConst.DSE_LINK_CHANNEL_APK.equals(linkChannel);

		if (!apk) {
			putAttrIfBlank(
					transactionAuditId,
					LoanOnCardConst.ATTR_DSE_BROWSER_NAME,
					firstNonBlank(mapVal(details, LoanOnCardConst.BROWSER_NAME),
							executionContext.getStringValue(LoanOnCardConst.BROWSER_NAME)));
			putAttrIfBlank(
					transactionAuditId,
					LoanOnCardConst.ATTR_DSE_BROWSER_VERSION,
					firstNonBlank(mapVal(details, LoanOnCardConst.BROWSER_VERSION),
							executionContext.getStringValue(LoanOnCardConst.BROWSER_VERSION)));
		}

		putAttrIfBlank(
				transactionAuditId,
				LoanOnCardConst.ATTR_DSE_SYSTEM_LOCATION,
				firstNonBlank(
						mapVal(details, LoanOnCardConst.SYSTEM_LOCATION),
						executionContext.getStringValue(LoanOnCardConst.SYSTEM_LOCATION),
						executionContext.getStringValue(TransactionAuditConstants.LOCATION)));
		putAttrIfBlank(
				transactionAuditId,
				LoanOnCardConst.ATTR_DSE_SYSTEM_OS_VERSION,
				firstNonBlank(mapVal(details, LoanOnCardConst.SYSTEM_OS_VERSION),
						executionContext.getStringValue(LoanOnCardConst.SYSTEM_OS_VERSION)));
		putAttrIfBlank(
				transactionAuditId,
				LoanOnCardConst.ATTR_DSE_SYSTEM_OS,
				firstNonBlank(mapVal(details, LoanOnCardConst.SYSTEM_OS),
						executionContext.getStringValue(LoanOnCardConst.SYSTEM_OS)));

		// DSE IP from gateway only (XFF / client_ip); FE browser_details does not carry IP.
		String dseIp =
				GatewayUsableClientIp.firstUsableFromGatewayPick(executionContext.getStringValue("client_ip"));
		putAttrIfBlank(transactionAuditId, LoanOnCardConst.ATTR_DSE_SYSTEM_IP_ADDRESS, dseIp);

		LOG.info(
				"LOC_MIS_DSE_DEVICE_PERSIST txn_id={} link_channel={} has_browser_details={}",
				transactionAuditId,
				linkChannel,
				details != null && !details.isEmpty());
	}

	/**
	 * Persist customer device fields from consent-status EC keys / API map. First-write-wins.
	 */
	public void persistCustomerDetailsFromConsentContext(long transactionAuditId, ExecutionContext executionContext) {
		if (transactionAuditId <= 0 || executionContext == null) {
			return;
		}
		persistCustomerDetails(
				transactionAuditId,
				executionContext.getStringValue(LoanOnCardConst.CONSENT_BROWSER_NAME),
				executionContext.getStringValue(LoanOnCardConst.CONSENT_BROWSER_VERSION),
				executionContext.getStringValue(LoanOnCardConst.CONSENT_SYSTEM_LOCATION),
				executionContext.getStringValue(LoanOnCardConst.CONSENT_SYSTEM_OS_VERSION),
				executionContext.getStringValue(LoanOnCardConst.CONSENT_SYSTEM_IP_ADDRESS),
				executionContext.getStringValue(LoanOnCardConst.CONSENT_SYSTEM_OS));
	}

	public void persistCustomerDetailsFromConsentApiMap(long transactionAuditId, Map<String, Object> apiResponseMap) {
		if (transactionAuditId <= 0 || apiResponseMap == null || apiResponseMap.isEmpty()) {
			return;
		}
		persistCustomerDetails(
				transactionAuditId,
				asString(apiResponseMap.get(LoanOnCardConst.CONSENT_BROWSER_NAME)),
				asString(apiResponseMap.get(LoanOnCardConst.CONSENT_BROWSER_VERSION)),
				asString(apiResponseMap.get(LoanOnCardConst.CONSENT_SYSTEM_LOCATION)),
				asString(apiResponseMap.get(LoanOnCardConst.CONSENT_SYSTEM_OS_VERSION)),
				asString(apiResponseMap.get(LoanOnCardConst.CONSENT_SYSTEM_IP_ADDRESS)),
				asString(apiResponseMap.get(LoanOnCardConst.CONSENT_SYSTEM_OS)));
	}

	private void persistCustomerDetails(
			long transactionAuditId,
			String browserName,
			String browserVersion,
			String location,
			String osVersion,
			String ip,
			String os) {
		putAttrIfBlank(transactionAuditId, LoanOnCardConst.ATTR_CUSTOMER_BROWSER_NAME, browserName);
		putAttrIfBlank(transactionAuditId, LoanOnCardConst.ATTR_CUSTOMER_BROWSER_VERSION, browserVersion);
		putAttrIfBlank(transactionAuditId, LoanOnCardConst.ATTR_CUSTOMER_SYSTEM_LOCATION, location);
		putAttrIfBlank(transactionAuditId, LoanOnCardConst.ATTR_CUSTOMER_SYSTEM_OS_VERSION, osVersion);
		putAttrIfBlank(transactionAuditId, LoanOnCardConst.ATTR_CUSTOMER_SYSTEM_IP_ADDRESS, ip);
		putAttrIfBlank(transactionAuditId, LoanOnCardConst.ATTR_CUSTOMER_SYSTEM_OS, os);
		LOG.info("LOC_MIS_CUSTOMER_DEVICE_PERSIST txn_id={}", transactionAuditId);
	}

	static String resolveDseLinkChannel(String channelCode) {
		if (StringUtils.isBlank(channelCode)) {
			return "";
		}
		if ("APP".equalsIgnoreCase(channelCode.trim())) {
			return LoanOnCardConst.DSE_LINK_CHANNEL_APK;
		}
		if ("WEB".equalsIgnoreCase(channelCode.trim())) {
			return LoanOnCardConst.DSE_LINK_CHANNEL_PWA;
		}
		return channelCode.trim().toUpperCase();
	}

	@SuppressWarnings("unchecked")
	private static Map<String, Object> resolveBrowserDetailsMap(ExecutionContext executionContext) {
		Object raw = executionContext.get(LoanOnCardConst.BROWSER_DETAILS);
		if (raw instanceof Map<?, ?> map) {
			return (Map<String, Object>) map;
		}
		return Map.of();
	}

	private void putAttrIfBlank(long transactionAuditId, String attrKey, String value) {
		String trimmed = StringUtils.trimToEmpty(value);
		if (StringUtils.isBlank(trimmed)) {
			return;
		}
		String existing = StringUtils.trimToEmpty(
				transactionAuditAttributesDAOService.findByTransactionAuditIdAndAttrKey(transactionAuditId, attrKey));
		if (StringUtils.isNotBlank(existing)) {
			return;
		}
		locUtils.createOrUpdateAttribute(transactionAuditId, attrKey, trimmed);
	}

	private static String mapVal(Map<String, Object> details, String key) {
		if (details == null || details.isEmpty()) {
			return "";
		}
		return asString(details.get(key));
	}

	private static String asString(Object value) {
		return value == null ? "" : StringUtils.trimToEmpty(String.valueOf(value));
	}

	private static String firstNonBlank(String... values) {
		if (values == null) {
			return "";
		}
		for (String v : values) {
			if (StringUtils.isNotBlank(v)) {
				return v.trim();
			}
		}
		return "";
	}
}
