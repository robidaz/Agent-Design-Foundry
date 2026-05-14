---
source_doc: partner_enablement_integration_guide.md
doc_type: partner_enablement
approval_status: approved
audience: integration_partners
---

# Partner Integration Guide — Dynamix Core Platform

This guide is the canonical reference for integration partners building against the Dynamix Core Platform. It is reviewed quarterly by the partner enablement team and is the authoritative source for the SDK, REST API, and webhook surfaces.

## API Surfaces

The Core Platform exposes three primary integration surfaces:

1. **REST API** — synchronous request/response, JSON over TLS 1.2+. Versioned via the `Accept: application/vnd.dynamix.v2+json` header. The v1 surface is supported for legacy partners through end-of-life 2026-12-31.
2. **Webhooks** — outbound HTTP POST callbacks for platform events (record-created, record-updated, workflow-completed, audit-event). Retries on 5xx response codes follow exponential backoff with a 1-second base and 12 attempts over approximately 4 hours before the event is dead-lettered.
3. **SDKs** — official client libraries are published for Python, Java, and TypeScript. The SDKs wrap the REST surface and add idempotency-key handling, paginated iterators, and retry policy.

## Authentication for Integrations

Integration partners authenticate using **service-account tokens** issued through the platform admin console. Tokens are scoped to a defined set of REST API permissions and an optional IP allow-list. SAML and OIDC are the user-facing identity-federation protocols; service-account tokens are the integration-facing equivalent and should not be conflated with end-user sessions.

For partners building user-impersonation flows (e.g. a partner portal authenticating end-customers against the customer's IdP), the standard pattern is SAML federation between the partner portal and the customer's IdP, followed by token-exchange against the platform's STS endpoint.

## Retry Semantics

All REST endpoints accept an `Idempotency-Key` header. The platform records the first response for a given key and returns the same response on subsequent requests with the same key within a 24-hour window. Partners are expected to set this header on any non-idempotent operation. The SDKs do this automatically.

Read-only endpoints are safe to retry unconditionally; writes without an idempotency key are not safe to retry and may produce duplicate records.

## Rate Limits

| Tier | Sustained req/s per token | Burst (≤ 10 s) |
| ---- | ------------------------- | -------------- |
| Standard | 200 | 500 |
| Enterprise | 1,000 | 2,500 |

Rate-limit responses (HTTP 429) include a `Retry-After` header in seconds; partners should respect it rather than implementing independent backoff.

## Sample Code

Code samples for the most common integration patterns (record sync, webhook receiver, paginated export) are published in the partner portal and updated with each minor release of the SDKs.
