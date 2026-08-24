#!/usr/bin/env python3
"""
Full Automated Deployment Script for 25-Aug-2026 across all sites
"""

import os
import subprocess
from update_ezconsultants_25_aug import update_ezconsultants

# 1. Update EZ Consultants
print("💼 Upgrading EZ Consultants...")
update_ezconsultants()

# 2. Update EZ Mortgage Broker
print("🏠 Upgrading EZ Mortgage Broker...")
os.system("python3 /Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/fix_aest_dates_and_sync.py")

# 3. Update PRO CRM
print("⚡ Upgrading PRO CRM...")
from publish_25_aug_all_sites import update_procrm
update_procrm()

print("🎉 Master sync complete!")
