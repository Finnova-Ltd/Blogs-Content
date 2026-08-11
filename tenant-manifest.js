/**
 * Multi-Tenant & Module Registry Manifest
 * Learned from Directus architectural patterns:
 * Enables dynamic registration of tenants, website origins, enabled CRM modules,
 * custom collection schemas, and REST endpoints across multiple websites.
 */

export const TENANT_MANIFEST = {
  version: "1.0.0",
  crm_engine: "digital-agent-platform",
  default_tenant: "finnova-charity",

  tenants: {
    "finnova-charity": {
      tenant_id: "finnova-charity",
      tenant_slug: "finnova",
      display_name: "Finnova Ltd — Digital Inclusion Charity",
      allowed_origins: ["https://finnova.org.au", "https://www.finnova.org.au", "http://localhost:8080"],
      enabled_modules: [
        "leads",
        "device_bank",
        "mygov_booking",
        "census_guidance",
        "grants_transparency",
        "cald_multilingual",
        "ai_advisor_chatbot"
      ],
      api_endpoints: {
        lead_intake: "/api/crm-lead",
        bookings: "/api?action=create_booking",
        device_eoi: "/api?action=submit_device_eoi"
      },
      audit_policy: {
        require_consent_flag: true,
        log_ip_address: false, // PII privacy protection
        retention_days: 730
      }
    },
    "jmloans-broker": {
      tenant_id: "jmloans-broker",
      tenant_slug: "jmloans",
      display_name: "JM Loans & Mortgage Broker",
      allowed_origins: ["https://jmloans.com.au", "http://localhost:5173"],
      enabled_modules: [
        "leads",
        "mortgage_calculator",
        "google_reviews",
        "appointments"
      ],
      api_endpoints: {
        lead_intake: "/api/google-reviews"
      },
      audit_policy: {
        require_consent_flag: true,
        log_ip_address: true,
        retention_days: 1095
      }
    },
    "ndis-desk-crm": {
      tenant_id: "ndis-desk-crm",
      tenant_slug: "ndis-desk",
      display_name: "NDIS Desk Operations Platform",
      allowed_origins: ["https://ndisdesk.com.au"],
      enabled_modules: [
        "leads",
        "participant_cockpit",
        "shift_costing",
        "compliance_vault"
      ],
      api_endpoints: {
        lead_intake: "/api/v1/leads"
      },
      audit_policy: {
        require_consent_flag: true,
        log_ip_address: true,
        retention_days: 2555
      }
    }
  }
};

/**
 * Helper to retrieve tenant metadata for an incoming request
 */
export function getTenantConfig(tenantIdOrSlug) {
  if (!tenantIdOrSlug) return TENANT_MANIFEST.tenants[TENANT_MANIFEST.default_tenant];
  const found = Object.values(TENANT_MANIFEST.tenants).find(
    t => t.tenant_id === tenantIdOrSlug || t.tenant_slug === tenantIdOrSlug
  );
  return found || TENANT_MANIFEST.tenants[TENANT_MANIFEST.default_tenant];
}

/**
 * Helper to check if a module is enabled for a specific tenant
 */
export function isModuleEnabled(tenantIdOrSlug, moduleName) {
  const tenant = getTenantConfig(tenantIdOrSlug);
  return tenant ? tenant.enabled_modules.includes(moduleName) : false;
}
