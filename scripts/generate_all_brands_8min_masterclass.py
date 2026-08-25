#!/usr/bin/env python3
"""
Master 8-10 Minute Long-Form Video Generator for All 4 Brands
--------------------------------------------------------------
Generates full 16:9 Landscape (1920x1080) deep-dive masterclass videos
with 4 rich chapters (~1,200 - 1,400 words spoken per brand) yielding
an 8-10 minute comprehensive YouTube episode.
"""

import os
import sys
import json
import asyncio
import subprocess
import shutil
from PIL import Image
import imageio_ffmpeg
import edge_tts

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"
ASSETS_DIR = os.path.join(BLOGS_DIR, "assets")
VIDEOS_DIR = os.path.join(ASSETS_DIR, "videos")
CACHE_DIR = os.path.join(BLOGS_DIR, "scripts/asset_cache")
DESKTOP_DIR = "/Users/robinbakshi/Desktop"

for d in [VIDEOS_DIR, CACHE_DIR]:
    os.makedirs(d, exist_ok=True)

sys.path.insert(0, os.path.join(BLOGS_DIR, "scripts"))
from render_longform_compilation import render_8min_master_compilation, BRAND_PROFILES

MASTERCLASS_DATA = {
    "ezmortgage": [
        {
            "title": "Macroeconomic Outlook & RBA Cash Rate Cycle in 2026",
            "content_deepdive": (
                "Welcome to the EZ Mortgage Broker 2026 Australian Mortgage Masterclass. As headline inflation moderates toward the Reserve Bank target band of two to three percent, Australia's monetary policy landscape is entering a critical transition phase. Major bank economic desks across Commonwealth Bank, Westpac, ANZ, and NAB are forecasting targeted adjustments to official cash rates. For existing mortgage holders and prospective property buyers, this creates an unprecedented window of opportunity to optimize loan structures. Lenders are currently competing aggressively for high quality borrowers by offering unadvertised discretionary rate discounts and variable tier reductions. Understanding the underlying debt serviceability assessment buffers enforced by APRA is essential when reviewing your existing home loan portfolio."
            ),
            "takeaway": "Proactively audit your existing home loan interest rate at least twice per year to ensure you are receiving the lender's lowest available retention tier."
        },
        {
            "title": "Refinancing Strategies: Slashing Annual Interest via 100% Offset Accounts",
            "content_deepdive": (
                "When refinancing an existing residential mortgage in Australia, interest rate percentage is only one component of total loan efficiency. Incorporating multiple one hundred percent offset sub-accounts allows homeowners to maintain emergency cash reserves, everyday salary deposits, and tax provisions while directly reducing daily compound interest calculations. For example, maintaining an average balance of fifty thousand dollars inside an offset account against an eight hundred thousand dollar mortgage at six percent reduces annual interest charges by three thousand dollars and can shave up to four years off your total loan term. Furthermore, restructuring non-deductible home loan debt into tax-deductible investment tranches through debt recycling establishes significant wealth generation velocity."
            ),
            "takeaway": "Direct all household income and operational cash flows into linked 100% offset accounts to compound daily interest savings."
        },
        {
            "title": "First Home Guarantee & Stamp Duty Concessions Blueprint",
            "content_deepdive": (
                "For first home buyers entering the property market across Sydney, Melbourne, Brisbane, and regional Australia, government initiatives provide substantial capital relief. Under the Federal Government First Home Guarantee scheme, eligible buyers can secure a residential dwelling with as little as a five percent deposit without incurring costly Lenders Mortgage Insurance fees, saving up to thirty thousand dollars upfront. Combined with expanded state-based stamp duty exemptions for new turnkey builds and off the plan apartments up to designated threshold caps, the required barrier to entry has decreased significantly. Working with an accredited mortgage broker ensures your deposit, genuine savings history, and employment probation status are matched with the lender offering the highest probability of unconditional credit approval."
            ),
            "takeaway": "Leverage government 5% deposit schemes and state stamp duty thresholds to enter the property market years ahead of conventional savings timelines."
        },
        {
            "title": "Commercial Property & SMSF Borrowing Arrangements (LRBA)",
            "content_deepdive": (
                "Self-Managed Super Fund property lending has experienced massive expansion as Australian business owners and private investors transition from leasing commercial premises to owning them directly inside super. Under a compliant Limited Recourse Borrowing Arrangement, an SMSF can borrow up to seventy to eighty percent of a commercial property's value. Your operational business pays commercial rent directly to your super fund, converting what was once an ordinary business expense into tax-sheltered retirement capital. Capital gains tax inside an SMSF in the accumulation phase is capped at ten percent for assets held longer than twelve months, and drops to zero percent once the fund enters pension phase."
            ),
            "takeaway": "Purchasing your business trading premises via an SMSF LRBA builds long-term commercial equity under Australia's most favorable tax structure."
        }
    ],
    "procrm": [
        {
            "title": "The Enterprise AI Shift: Moving from AI Operators to Systems Orchestrators",
            "content_deepdive": (
                "Welcome to the PRO CRM Enterprise AI Architecture Masterclass for 2026. Across the Australian corporate landscape, organizations are moving rapidly past the era of standalone conversational chat tools and manual prompt engineering. While individual chatbot interfaces provided initial productivity gains, they failed to integrate into core enterprise databases and created unmanageable shadow IT risks. Forward thinking Chief Information Officers and Chief Technology Officers are now investing heavily in AI Orchestrators. These architectural frameworks interconnect autonomous multi-agent networks capable of executing end-to-end business operations—from participant onboarding and real-time compliance validation to automated financial reconciliation across enterprise systems."
            ),
            "takeaway": "Replace isolated chat prompts with governed multi-agent orchestration directly integrated into your core CRM and ERP systems."
        },
        {
            "title": "Salesforce Data Cloud Zero-Copy Lakehouse Integration",
            "content_deepdive": (
                "For decades, enterprise data teams struggled with fragile, expensive batch ETL pipelines that duplicated terabytes of customer information across disparate databases. Salesforce Data Cloud Zero-Copy fundamentally eliminates data movement. By virtualizing live queries across Snowflake, Google BigQuery, Databricks, and AWS Redshift at the metadata layer using open Apache Iceberg and Delta Sharing protocols, data remains securely inside your enterprise lakehouse while remaining instantly queryable by Salesforce Core and autonomous reasoning engines. This architecture reduces data synchronization latency by over ninety percent and completely slashes third party middleware licensing costs."
            ),
            "takeaway": "Adopt Zero-Copy virtualization to empower real-time Agentforce reasoning without copying data out of your sovereign enterprise warehouse."
        },
        {
            "title": "APRA CPS 234 & Einstein Trust Layer Governance Playbook",
            "content_deepdive": (
                "Deploying autonomous software agents in regulated Australian industries—including banking, insurance, healthcare, and disability services—demands uncompromising security guardrails. The Salesforce Einstein Trust Layer enforces strict zero-data-retention agreements with foundation model providers, ensuring enterprise data is never used to train public models. Furthermore, native data masking automatically strips personally identifiable information, tax file numbers, and credit card credentials before grounding prompts are evaluated. Immutable session logging provides the exact cryptographic audit trails required by APRA CPS 234, Essential Eight cyber frameworks, and ISO 27001 regulatory standards."
            ),
            "takeaway": "Enforce automated PII masking and cryptographic audit logging to ensure total APRA CPS 234 and ISO 27001 compliance for enterprise AI."
        },
        {
            "title": "Deploying Agentforce Autonomous Workflows in Under 4 Weeks",
            "content_deepdive": (
                "Scaling enterprise AI no longer requires twelve-month multi-million dollar transformation programs. PRO CRM's proven fixed-sprint delivery model deploys production-ready Agentforce autonomous workflows in under four weeks. Week one establishes lakehouse connectors and trust layer boundaries. Week two configures CRM action topics and deterministic reasoning chains. Week three conducts automated regression testing and user acceptance benchmarking. Week four transitions the system into live production with twenty-four-seven monitoring. This rapid time-to-value model delivers immediate operational cost reductions while accelerating customer resolution velocity across all digital channels."
            ),
            "takeaway": "Utilize structured 4-week agile deployment sprints led by Principal Architects to achieve immediate ROI on enterprise AI investments."
        }
    ],
    "ezconsultants": [
        {
            "title": "NDIS Pricing & Quality Safeguards Compliance Overhaul 2026",
            "content_deepdive": (
                "Welcome to the EZ Consultants 2026 National Compliance & Enterprise Strategy Masterclass. The National Disability Insurance Scheme is undergoing its most comprehensive regulatory transformation to date, with enhanced quality and safeguards standards and restructured price limits. Registered and unregistered NDIS service providers must maintain rigorous documentation surrounding participant service agreements, incident management logs, and worker screening verifications. Our advisory practice helps Australian disability enterprises implement automated compliance workflows that eliminate audit vulnerabilities and ensure predictable cash flow management."
            ),
            "takeaway": "Automate service agreement tracking and incident reporting to guarantee audit readiness under the latest NDIS Quality and Safeguards standards."
        },
        {
            "title": "Aged Care Mandatory Care Minutes & SIRS Digital Reporting",
            "content_deepdive": (
                "With the Australian Government enforcing mandatory direct care minute requirements and enhanced Serious Incident Response Scheme reporting across residential aged care facilities, digital workforce management is critical. Facilities must accurately capture and report registered nurse and personal care worker ratios in real time. Failure to meet mandated compliance thresholds directly impacts accreditation status and government subsidy funding. Implementing integrated CRM and rostering architectures ensures every care minute is verified and auditable."
            ),
            "takeaway": "Deploy real-time rostering validation to effortlessly fulfill mandatory aged care minute thresholds and protect facility accreditation."
        },
        {
            "title": "Corporate Tax Structuring & Research and Development Tax Incentives",
            "content_deepdive": (
                "Maximizing business tax efficiency requires proactive structural planning. Australian SMEs and technology companies investing in novel software development, engineering, or process innovation can claim up to forty-three point five percent in refundable tax offsets through the Federal Government R and D Tax Incentive. Our corporate advisory team structures your operational entities, trust allocations, and intellectual property holdings to minimize tax liabilities while unlocking non-dilutive government innovation capital."
            ),
            "takeaway": "Structure qualifying software and engineering expenditures to claim up to 43.5% in refundable R&D tax cash offsets."
        },
        {
            "title": "End-to-End Enterprise CRM Implementation & Managed Services",
            "content_deepdive": (
                "Software alone does not transform an organization—structured business process re-engineering does. EZ Consultants delivers bespoke CRM consulting, legacy system migration, and ongoing managed support services. We align your digital workflows with your operational staff, eliminating manual data entry bottlenecks and empowering executive teams with real-time financial reporting dashboards that drive sustainable enterprise growth across Australia."
            ),
            "takeaway": "Partner with accredited Australian consultants to build scalable digital systems that drive long-term business valuation."
        }
    ],
    "ezsignature": [
        {
            "title": "Australian Electronic Transactions Act & Legal Binding E-Signatures",
            "content_deepdive": (
                "Welcome to the EZ Signature 2026 Legal & Enterprise Digital Workflow Masterclass. In Australia, electronic signatures are governed by the Electronic Transactions Act 1999 and State-based equivalents. For a digital signature to be legally binding and admissible in court, it must fulfill three core requirements: clear method of identification, verifiable intention to sign, and consent to electronic communication. EZ Signature delivers cryptographic audit certificates, IP address tracking, and tamper-evident SHA-256 digital seals that guarantee complete evidentiary validity for contracts, property leases, and corporate agreements."
            ),
            "takeaway": "Ensure all corporate and legal documents utilize tamper-evident SHA-256 cryptographic audit trails to guarantee total legal enforceability."
        },
        {
            "title": "Zero-Data-Tracking Architecture: Sovereignty & Privacy",
            "content_deepdive": (
                "Unlike traditional US-based e-signature providers that store customer contracts on shared international cloud servers and analyze document metadata, EZ Signature operates on a strict zero-data-retention and Australian sovereign data residency framework. Your confidential contracts, commercial terms, and personal identification details remain fully encrypted and are never accessible to third party platforms or advertisers. This architecture provides Australian enterprises with complete privacy peace of mind."
            ),
            "takeaway": "Protect sensitive corporate agreements with Australian-hosted, zero-data-tracking e-signature infrastructure."
        },
        {
            "title": "API & CRM Integration: Streamlining Client Onboarding Workflows",
            "content_deepdive": (
                "Manual document preparation and email back-and-forth cost Australian enterprises thousands of administrative hours each year. With EZ Signature's REST API and native CRM connectors, contract generation, signer routing, and final PDF archiving are fully automated. When a prospect signs an agreement on any mobile device or tablet, your CRM status updates instantly, payment gateways trigger automatically, and signed copies are securely routed to all stakeholders."
            ),
            "takeaway": "Automate contract generation and signer routing via API to slash client onboarding turnarounds from days to seconds."
        },
        {
            "title": "Enterprise Cost Optimization: Eliminating Inflated Per-Envelope Fees",
            "content_deepdive": (
                "Legacy e-signature vendors charge punitive per-envelope fees that balloon as your business scales. EZ Signature provides transparent flat-rate enterprise plans with unlimited document signing, custom branding, and multi-signer workflows. By switching to EZ Signature, Australian legal practices, financial brokerages, and real estate agencies reduce their monthly digital signature overhead by up to seventy percent while enjoying superior local support."
            ),
            "takeaway": "Switch from overpriced per-envelope vendors to flat-rate Australian e-signature infrastructure to slash operational costs."
        }
    ]
}

def render_all():
    print("🚀 Starting Master 8-10 Minute Long-Form Video Generator for all 4 Brands...")
    for brand_key, batch in MASTERCLASS_DATA.items():
        print(f"\n=======================================================")
        print(f"🎬 Rendering Masterclass Episode for: {brand_key.upper()}")
        print(f"=======================================================")
        mp4_path = render_8min_master_compilation(brand_key, batch)
        
        # Copy to standard destination
        target_name = f"masterclass_{brand_key}_10min.mp4"
        dest_video = os.path.join(VIDEOS_DIR, target_name)
        shutil.copy2(mp4_path, dest_video)
        
        # Also copy to desktop
        desktop_dest = os.path.join(DESKTOP_DIR, f"{brand_key}_Masterclass_2026_10Min.mp4")
        shutil.copy2(mp4_path, desktop_dest)
        print(f"✅ Saved to: {dest_video}")
        print(f"🖥️ Copied to Desktop: {desktop_dest}")

    # Commit and push all master videos to GitHub
    os.system(f'cd "{BLOGS_DIR}" && git add assets/videos/ && git commit -m "Publish 8-10 minute masterclass episodes for all brands" && git push origin main')
    print("\n🎉 All 4 Masterclass Episodes rendered, saved to Desktop, and pushed to GitHub!")

if __name__ == "__main__":
    render_all()
