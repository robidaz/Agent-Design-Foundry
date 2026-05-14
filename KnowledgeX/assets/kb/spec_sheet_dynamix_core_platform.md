---
source_doc: spec_sheet_dynamix_core_platform.md
doc_type: spec_sheet
approval_status: approved
product: Dynamix Core Platform
release_line: 2025.x
---

# Dynamix Core Platform — Specification Sheet (2025.x)

The Dynamix Core Platform is the central control-plane and data-management tier of the Dynamix product family. This document is the authoritative reference for platform capabilities, supported protocols, and operating limits in the 2025.x release line.

## Identity and Access

The Core Platform supports two identity-federation protocols for enterprise integration:

- **SAML 2.0** — supported on all 2024.x and 2025.x releases. Group-to-role mapping is performed via SAML attribute statements.
- **OIDC (OpenID Connect)** — supported on 2025.x and later. Group-to-role mapping uses standard OIDC claims and the same admin-console configuration as SAML.

Local accounts are supported for emergency-access scenarios but are disabled by default in production deployments. Multi-factor authentication is enforced when the identity provider supports it.

## Encryption

- **At rest:** AES-256-GCM is the default cipher for all data on disk, including primary database storage, snapshot archives, and audit logs. The 2025.x release introduced support for customer-managed keys via HSM integration (PKCS#11 and KMIP). Earlier releases supported only platform-managed keys.
- **In transit:** TLS 1.2 minimum on all platform-internal and external interfaces. TLS 1.3 is supported and is the negotiated default when both peers support it. FIPS 140-2 validated mode is available via the `--security-profile=fips` provisioning flag.

## Audit Logging

All administrative actions, authentication events, and configuration changes are written to an append-only audit log. The audit log is integrity-signed using the platform key hierarchy and is immutable once written. Retention is configurable from 90 days to 2,555 days (seven years); the default is 365 days.

## Recovery Profiles

Two recovery profiles are documented for the 2025.x release line:

1. **Standard profile** — asynchronous replication; RPO 15 minutes; RTO 4 hours single-region.
2. **High-Availability profile** — synchronous replication between availability zones; RPO 5 minutes; RTO 90 minutes in-region failover. Requires a multi-AZ deployment.

The recovery profile is selected at deployment time and is not switchable in place.

## Operating Limits

| Limit | Standard tier | Enterprise tier |
| ----- | ------------- | --------------- |
| Concurrent active users | 5,000 | 25,000 |
| Sustained API requests / second | 2,500 | 12,000 |
| Maximum dataset size | 50 TB | 500 TB |
| Snapshot retention | 30 days | 365 days |

## Supported Platforms

Linux x86_64 (RHEL 8 / 9, Ubuntu 22.04 LTS) and ARM64 (RHEL 9 only). Windows Server is not a supported platform for the Core tier; partner-enablement guidance covers Windows-side integration via the SDK.
