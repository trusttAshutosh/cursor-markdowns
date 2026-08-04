# JSDoc Examples (Repo-Aligned)

Concrete patterns from this codebase. Use as templates when adding docs to new or modified code.

---

## Helper — `src/helpers/requestBodyHeaders.ts`

```typescript
/**
 * Returns request headers.
 *
 * @param type - omit (or any other value) → body headers for v1 APIs (plain object)
 *               "http" → HTTP headers for v2 APIs (keys auto-converted to x-{key})
 */
export function getRequestBodyHeaders(type?: string): Record<string, any> { ... }
```

## Helper — `src/helpers/firebaseHelper.ts`

```typescript
/**
 * Merges current data from Firebase with new update data, encrypts it, and updates the Firestore document.
 *
 * @param docId - Document ID
 * @param updateObject - Data to update
 * @param isCobrowsingEnabled - Flag to enable/disable cobrowsing
 * @returns Promise that resolves when the document is updated
 */
export const updateFirebase = async (
  docId: string,
  updateObject: object,
  isCobrowsingEnabled = true,
  ...
): Promise<void> => { ... };
```

---

## Hook — `src/components/Screens/Journeys/LOC/hooks/useLOCConsent.ts`

Hook-level summary + `@returns`; internal helpers get short summaries only when non-obvious.

```typescript
/**
 * Manages LOC consent sending, journey initialization, and navigation to the waiting screen.
 * @returns Consent API helpers, agent-detail builders, and journey navigation methods.
 */
const useLOCConsent = () => {
  /** Builds agent details object for customer-assisted journeys. */
  const buildAgentDetails = (): AgentDetails | null => { ... };

  /** Sends customer consent request. */
  const sendConsent = async ({ ... }: SendConsentParams) => { ... };

  return {
    sendConsent,
    buildAgentDetails,
    getTemplateCode,
    initializeJourneyData,
    navigateToConsentWaiting,
    assistType,
    loginDetails,
  };
};
```

## Hook — `src/Config/customHooks/useApi.tsx` (target pattern)

`useApi` currently lacks JSDoc. When modifying it, add:

```typescript
/**
 * Provides GET/POST API helpers with session-timeout handling and diagnostic logging.
 * @returns Loading and error state plus `doGet` and `doPost` request methods.
 */
const useApi = (): UseApiReturnType => { ... };
```

---

## Context — `src/context/CoBrowsingContext.tsx` (target pattern)

Provider has no JSDoc today. When modifying it, add:

```typescript
/**
 * Syncs co-browsing Firestore state with Redux and exposes Firebase dispatch helpers to journey screens.
 */
export const CobrowsingProvider = ({
  docId,
  isAgent,
  children,
  isCobrowsingEnabled,
}: Props) => { ... };
```

## Interceptor — `src/Config/axios/requestInterceptor/headerConsolidationInterceptor.ts`

```typescript
/**
 * Bundles all custom x- headers into one x-app-context header to bypass WAF limits.
 * Must be the last request interceptor to run.
 *
 * @param config - Axios request config; reads metadata.stan and mutates headers.
 * @returns Modified request config with consolidated x-app-context header.
 */
const headerConsolidationInterceptor = async (config: any) => { ... };
```

---

## Component props — `src/components/pages/DiyLandingScreen/DiyVerificationScreenView.tsx`

Per-prop JSDoc on non-obvious fields; omit docs on self-explanatory props.

```typescript
export interface DiyVerificationViewProps {
  /** Current step: "select" | "loading" */
  step: "select" | "loading";
  /** Loading text for the waiting state */
  loadingText: string;
  /** Verification options to display */
  verificationTypes: VerificationType[];
  /** Currently selected verification type (null = none) */
  selectedType: VerificationType | null;
  /** Callback when user selects a card */
  onSelectType: (type: VerificationType) => void;
  /** Callback when user clicks Continue */
  onContinue: () => void;
  customerMobileNumber?: string;
  clientReferenceNumber?: string;
}
```

## Common component — `src/components/common/**` (target pattern)

When adding or modifying shared components, follow this shape:

```typescript
export interface NPSelectProps {
  /** Label shown above the select field. */
  label: string;
  /** Called when the selected option changes. */
  onChange: (value: string) => void;
  options: NPSelectOptionType[];
}

/**
 * Renders a styled MUI select integrated with react-hook-form and project-standard validation display.
 */
function NPSelect(props: Readonly<NPSelectProps>) { ... }
```

---

## TypeScript Examples

Before/after patterns for new or modified code. See also `typescript-react-strict.mdc` and `typescript-react-components.mdc`.

### Redux — `state: any` → `RootState`

**Before** (legacy pattern in hooks):

```typescript
import { useSelector } from "react-redux";

const actorId = useSelector((state: any) => state.loginDetails.actorId);
```

**After** (required on new/modified selectors):

```typescript
import { useSelector } from "react-redux";
import { RootState } from "../../Config/store";

const actorId = useSelector((state: RootState) => state.loginDetails.actorId);
```

Use `useDispatch<AppDispatch>()` the same way when dispatching typed thunks or actions.

### Callback — bare `Function` → typed signature

**Before** (`src/components/common/Forms.types.ts` legacy):

```typescript
export interface NPInputType {
  onChange?: Function;
  onBlur?: Function;
}
```

**After** (when modifying common input props):

```typescript
import { ChangeEvent, FocusEvent } from "react";

export interface NPInputType {
  onChange?: (event: ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (event: FocusEvent<HTMLInputElement>) => void;
}
```

For MUI selects, use `SelectChangeEvent<string>` from `@mui/material`.

### Service — add `*Response` interface

**Before** (new endpoint with loose typing):

```typescript
export const fetchCustomerDetails = async (customerId: string) => {
  const response = await axiosInstance.post("/customer/details", { customerId });
  return response.data;
};
```

**After** (required on new/modified service methods):

```typescript
interface CustomerDetailsRequest {
  customerId: string;
}

interface CustomerDetailsResponse {
  customer_name: string;
  mobile_number: string;
  response_status: { code: string; message: string };
}

export const fetchCustomerDetails = async (
  customerId: string,
): Promise<CustomerDetailsResponse> => {
  const body: CustomerDetailsRequest = { customerId };
  const response = await axiosInstance.post<CustomerDetailsResponse>(
    "/customer/details",
    body,
  );
  return response.data;
};
```

Colocate `*Request` / `*Response` in the same file or a sibling `*.types.ts`.

### Hook — explicit return type + `unknown` error

**Before** (`useApi.tsx` legacy):

```typescript
interface UseApiReturnType {
  isLoading: boolean;
  error: any;
  doPost: (url: string, requestBody: any, headers?: RequestHeaders) => Promise<ApiResponse>;
}

const useApi = () => { ... };
```

**After** (when modifying the hook):

```typescript
interface UseApiReturn {
  isLoading: boolean;
  error: unknown;
  doGet: (url: string) => Promise<ApiResponse>;
  doPost: (
    url: string,
    requestBody: Record<string, unknown>,
    headers?: RequestHeaders,
  ) => Promise<ApiResponse>;
}

const useApi = (): UseApiReturn => { ... };
```

### Interceptor — `config: any` → Axios types

**Before**:

```typescript
const headerConsolidationInterceptor = async (config: any) => { ... };
```

**After**:

```typescript
import type { InternalAxiosRequestConfig } from "axios";

const headerConsolidationInterceptor = async (
  config: InternalAxiosRequestConfig,
): Promise<InternalAxiosRequestConfig> => { ... };
```
