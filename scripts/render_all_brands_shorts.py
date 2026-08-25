#!/usr/bin/env python3
import os
import sys
import shutil

BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"
sys.path.insert(0, os.path.join(BLOGS_DIR, "scripts"))
from render_ultimate_short import render_ultimate_video

print("🎬 Rendering EZ Signature Short...")
sig_mp4 = render_ultimate_video(
    title="Enterprise Digital Signatures AU",
    sentences=[
        "Are you still using manual paperwork for enterprise agreements?",
        "EZ Signature delivers APRA compliant, legally binding e-signatures with zero data tracking.",
        "Visit ezsignature.com today to streamline your client onboarding workflows."
    ],
    brand_key="ezsignature"
)
dest_sig = os.path.join(BLOGS_DIR, "assets", "videos", "ezsignature_enterprise_compliance.mp4")
shutil.copy2(sig_mp4, dest_sig)

print("🎬 Rendering EZ Consultants Short...")
cons_mp4 = render_ultimate_video(
    title="NDIS Software & Aged Care Compliance",
    sentences=[
        "Navigating NDIS quality safeguards and mandatory care minutes?",
        "EZ Consultants provides end-to-end CRM and workforce compliance systems across Australia.",
        "Contact our principal advisory team today at 1300 050 099."
    ],
    brand_key="ezconsultants"
)
dest_cons = os.path.join(BLOGS_DIR, "assets", "videos", "ezconsultants_compliance_blueprint.mp4")
shutil.copy2(cons_mp4, dest_cons)

os.system(f'cd "{BLOGS_DIR}" && git add assets/videos/ scripts/ && git commit -m "Add EZ Signature and EZ Consultants Short MP4s" && git push origin main')
print("🚀 All brand videos rendered, committed, and pushed to GitHub!")
