# TODO

This file tracks the delta between what the documentation promises and what is
actually implemented in the codebase. Use it as a guide for future development.

For the full development roadmap, see [docs/development/roadmap.md](docs/development/roadmap.md).
For detailed milestone specifications, see [docs/milestones.md](docs/milestones.md).

---

## Implemented (Working)

These features are documented and confirmed working in the codebase:

- [x] **DMARC Aggregate Report Parsing** — XML, ZIP, and GZIP formats supported
      via `defusedxml` (`backend/app/services/dmarc_parser.py`)
- [x] **Report Upload** — Web interface for uploading DMARC reports with multi-layer
      file validation; parsed reports are currently stored in the in-memory
      `ReportStore` (`backend/app/api/api_v1/endpoints/reports.py`,
      `backend/app/services/report_store.py`)
- [x] **IMAP Integration** — Auto-fetch reports from mailbox with background
      scheduler; ingested reports are currently stored in the in-memory
      `ReportStore` (`backend/app/services/imap_client.py`)
- [x] **Basic Dashboard** — Domain overview with compliance stats, Chart.js
      visualizations on domain detail page; data is sourced from the in-memory
      report store and live DNS checks (`backend/app/templates/`)
- [x] **Security Hardening** — Authentication middleware, security headers (CSP,
      HSTS, X-Frame-Options), defusedxml for XXE protection, restricted CORS,
      sanitized error responses (`backend/app/middleware/security.py`,
      `backend/app/core/security.py`)
- [x] **Docker Deployment Scaffolding** — Docker Compose and backend image setup
      exist for local/containerized deployment, but production hardening remains
      to be completed
      (`docker-compose.yml`, `backend/Dockerfile`)
- [x] **Setup Wizard** — Basic guided onboarding endpoints, though in-memory only
      (`backend/app/api/api_v1/endpoints/setup.py`)
- [x] **DNS Record Health Checks** — Real DNS lookups for DMARC, SPF, DKIM, and
      reverse-DNS (PTR) via `SystemDNSProvider` (dnspython async) and
      `CloudflareDNSProvider` (DNS-over-HTTPS); used by `/dns`, `/summary`, and
      `/sources` API endpoints (`backend/app/services/dns_resolver.py`)

---

## Documented but NOT Implemented

The following features are described in the README, documentation, or roadmap but
have no working implementation in the codebase yet.

### Database-Backed Report Persistence
- **Documented in**: TODO.md ("Database Persistence"), backend SQLAlchemy models,
  and Alembic migrations.
- **Current state**: SQLAlchemy configuration, models, and migrations exist, but
  uploaded and IMAP-ingested DMARC reports are stored in the in-memory
  `ReportStore`. Data is lost on process restart and is not shared across app
  instances.
- [ ] Persist uploaded reports, report records, domain summaries, and source data
      through SQLAlchemy models
- [ ] Update dashboard, reports, domains, DNS selector, and source endpoints to
      read from the database instead of `ReportStore`
- [ ] Add duplicate-report detection at the database layer
- [ ] Add migration/backfill path if any existing deployments need in-memory or
      exported report data imported

### Production-Ready Docker Deployment
- **Documented in**: TODO.md ("Docker Deployment") and deployment docs.
- **Current state**: `docker-compose.yml` and `backend/Dockerfile` exist, but the
  compose file is configured like a development stack: source bind mount,
  `DEBUG=True`, `ENVIRONMENT=development`, hardcoded database credentials, and a
  placeholder `SECRET_KEY`.
- [ ] Add a production Compose profile or separate production Compose file
- [ ] Remove source bind mounts from production deployment
- [ ] Move secrets and database credentials to environment files or secret
      management
- [ ] Set production-safe defaults for `DEBUG`, `ENVIRONMENT`, auth, CORS, and
      TLS/proxy headers
- [ ] Document production upgrade, backup, and migration flow

### Cloudflare Integration
- **Documented in**: README.md ("Cloudflare-integrated"), docs/development/roadmap.md (Milestone 8)
- **Current state**: Configuration variables exist in `backend/app/core/config.py`
  (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ZONE_ID`) but no functional code uses them.
- [ ] Automatic domain discovery from Cloudflare account
- [ ] Fetch and analyze DNS records via Cloudflare API
- [ ] Suggest missing or malformed DNS entries
- [ ] Track configuration changes over time

### Alerts & Notifications (Apprise)
- **Documented in**: README.md ("Integration with Apprise"), docs/development/roadmap.md (Milestone 6)
- **Current state**: `apprise>=1.4.5` is listed in `backend/requirements.txt` but
  is never imported or used anywhere in the codebase.
- [ ] Apprise integration for multi-channel notifications
- [ ] Email, Slack, webhook alert delivery
- [ ] Alert on new failures, compliance drops, or unknown senders
- [ ] Customizable alert rules and notification preferences
- [ ] Alert history and management

### Forensic Reports (RFC 6591)
- **Documented in**: README.md ("Forensic Reports: Analyze failure samples (RFC 6591 support)")
- **Current state**: The DMARC parser (`backend/app/services/dmarc_parser.py`) only
  handles aggregate reports. There is no forensic report parsing, UI, or storage.
- [ ] Forensic report parsing
- [ ] Failure sample analysis
- [ ] PII redaction options
- [ ] Detailed authentication failure views

### User Authentication & Multi-User Support
- **Documented in**: README.md ("Built-in authentication via FastAPI Users"),
  docs/development/roadmap.md (Milestone 5)
- **Current state**: A `User` model exists (`backend/app/models/user.py`) and
  `fastapi-users[sqlalchemy]` is in requirements, but FastAPI-Users is never wired
  up. There are no registration, login, or password-reset endpoints. Admin auth is
  API-key based only.
- [ ] User registration and login endpoints
- [ ] JWT-based session authentication for end users
- [ ] Password reset functionality
- [ ] Role-based access control (RBAC) per domain
- [ ] Multi-factor authentication (MFA)
- [ ] Email verification

### Dashboard Visualizations (Real Data)
- **Documented in**: README.md ("Track pass/fail rates over time", "Volume & Trends")
- **Current state**: Stats endpoints (`backend/app/utils/stats_summarizer.py`,
  `backend/app/api/api_v1/endpoints/domains.py`) now query real data from the
  database and in-memory ReportStore. Chart.js visualizations display actual
  compliance trends derived from uploaded DMARC reports.
- [x] Historical trend charts with real data
- [x] Compliance rate visualizations from actual reports
- [x] Volume and sender analytics based on stored data
- [x] Time-series data from database
- [x] Domain comparison views

### Advanced Rule Engine
- **Documented in**: docs/development/roadmap.md (Milestone 7)
- **Current state**: Not implemented at all.
- [ ] Custom alert conditions
- [ ] Threshold-based triggers
- [ ] New sender detection
- [ ] Anomaly detection

### Advanced Analytics & Reporting
- **Documented in**: docs/development/roadmap.md (Milestone 10)
- **Current state**: Not implemented at all.
- [ ] Historical trend analysis
- [ ] Comparative reporting
- [ ] Export capabilities (PDF, CSV)
- [ ] Scheduled reports
- [ ] Custom dashboards

### Enterprise Features
- **Documented in**: docs/development/roadmap.md (Milestone 11)
- **Current state**: Not implemented at all.
- [ ] Multi-tenant architecture
- [ ] API rate limiting (beyond basic)
- [ ] Advanced RBAC
- [ ] SSO integration (SAML, OAuth)
- [ ] Compliance reporting (SOC 2, GDPR)

### Real-Time Features
- **Documented in**: README.md ("real-time insights")
- **Current state**: No WebSocket or real-time push functionality exists.
- [ ] WebSocket or SSE for live dashboard updates

---

## Partially Implemented

### Setup Wizard
- **Status**: Endpoints exist (`/api/v1/setup/status`, `/api/v1/setup/admin`,
  `/api/v1/setup/system`) but store data in memory only. Not persisted to database.
- [ ] Persist setup configuration to database
- [ ] Complete guided onboarding flow in the UI

### IMAP Credential Security
- **Status**: IMAP integration works but credential storage needs improvement.
- [ ] Encrypt IMAP credentials at rest
- [ ] Add vault integration for secure credential storage
- [ ] Audit logging for IMAP operations

### DNS Record Health Checks
- **Documented in**: README.md ("Inspect SPF, DKIM, DMARC, MX, and BIMI records"),
  docs/development/roadmap.md (Milestone 8)
- **Current state**: The `/api/v1/domains/{domain_id}/dns` and `/api/v1/domains/summary`
  endpoints perform real DNS lookups via `SystemDNSProvider` (dnspython async) and
  `CloudflareDNSProvider` (DNS-over-HTTPS), implemented in
  `backend/app/services/dns_resolver.py`. DKIM selectors from DMARC reports and manually
  configured selectors are both checked. PTR reverse-DNS lookups power the `/sources`
  endpoint. Full Cloudflare zone-management integration is planned for a future milestone.
- [x] Real DNS lookups for SPF, DKIM, and DMARC records
- [x] Proper error handling for DNS failures and timeouts (per-domain timeouts, graceful fallback)
- [x] Unit and integration tests for DNS resolution (55 tests passing)
- [ ] MX record lookups
- [ ] BIMI record support
- [ ] Cloudflare API zone-management integration (read/write DNS records)
- [ ] Provider-specific fix suggestions (Google, Microsoft, etc.)
- [ ] DNSSEC validation

---

## Housekeeping

- [ ] Remove unused `apprise` from `requirements.txt` or implement alerts
- [x] Remove unused `dnspython` from `requirements.txt` or implement DNS checks (done — `dnspython` is used by `SystemDNSProvider`)
- [ ] Remove or wire up `fastapi-users` (currently installed but unused)
- [x] Replace mock data in stats endpoints with real database queries
- [x] Replace mock DNS data with actual DNS lookups
- [x] Add CI/CD pipeline — GitHub Actions workflows in `.github/workflows/ci.yml`
        (lint → test/security/CodeQL/dependency-review → Docker build/push → GitOps)
        and `.github/workflows/release.yml` (semantic versioning)
- [ ] Reach >80% test coverage
