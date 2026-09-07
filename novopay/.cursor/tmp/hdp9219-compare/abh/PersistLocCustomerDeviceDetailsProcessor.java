package in.novopay.creditcard.loc.processors;

import in.novopay.creditcard.loc.util.LOCUtils;
import in.novopay.creditcard.loc.util.LocMisDeviceDetailsPersister;
import in.novopay.infra.platform.annotations.Processor;
import in.novopay.infra.platform.exception.NovopayFatalException;
import in.novopay.infra.platform.exception.NovopayNonFatalException;
import in.novopay.infra.platform.navigation.AbstractProcessor;
import in.novopay.infra.platform.navigation.ExecutionContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * HDP-9219: captures the customer device details for the LOC MIS from the request's
 * {@code browser_details} block, which the agent app relays verbatim from the
 * {@code getCustomerConsentStatus} response.
 *
 * <p>Wired into {@code common_loanOnCards.xml} under {@code getLOCOffers} only, so it runs on exactly
 * one API and writes only {@code customer_*} keys.
 *
 * <p>Runs after {@code loanOffersProcessor} so the transaction audit id exists. Never throws — a
 * MIS-capture failure must not fail the journey.
 */
@Processor
public class PersistLocCustomerDeviceDetailsProcessor extends AbstractProcessor {

    private static final Logger LOG = LoggerFactory.getLogger(PersistLocCustomerDeviceDetailsProcessor.class);

    private final LOCUtils locUtils;
    private final LocMisDeviceDetailsPersister deviceDetailsPersister;

    public PersistLocCustomerDeviceDetailsProcessor(
            LOCUtils locUtils, LocMisDeviceDetailsPersister deviceDetailsPersister) {
        this.locUtils = locUtils;
        this.deviceDetailsPersister = deviceDetailsPersister;
    }

    @Override
    protected void process(ExecutionContext executionContext) throws NovopayFatalException, NovopayNonFatalException {
        try {
            Long txnAuditId = locUtils.resolveTransactionAuditId(executionContext);
            if (txnAuditId == null || txnAuditId <= 0) {
                LOG.info("LOC_MIS_CUSTOMER_DEVICE_PERSIST_SKIP reason=no_transaction_audit_id");
                return;
            }
            deviceDetailsPersister.persistCustomerDetails(txnAuditId, executionContext);
        } catch (Exception e) {
            LOG.warn("LOC_MIS_CUSTOMER_DEVICE_PERSIST_SKIP reason=unexpected_error message={}", e.getMessage());
        }
    }
}
