#!/usr/bin/env python3
"""
Inspect and add Sitemap link to footer across all 5 repos:
1. ezsignature.com (eSignaturesonline)
2. procrm.com.au (procrm-app)
3. ezconsultants.com.au
4. ezmortgagebroker.com.au
5. finnova.org.au (Finnova)
"""

import os
import glob
import re

# 1. ezsignature.com: Find footer in eSignaturesonline/frontend
ezsig_dir = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend/src"
for root, _, files in os.walk(ezsig_dir):
    for f in files:
        if f.endswith(('.jsx', '.js', '.tsx', '.ts')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as file:
                content = file.read()
            if 'Terms & Conditions' in content or 'Privacy Policy' in content:
                print(f"Found footer elements in ezsignature: {p}")

# 2. Check procrm-app
procrm_dir = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src"
for root, _, files in os.walk(procrm_dir):
    for f in files:
        if f.endswith(('.jsx', '.js', '.tsx', '.ts')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as file:
                content = file.read()
            if 'Privacy Policy' in content or 'Terms of Service' in content or '© 2026 PRO CRM' in content:
                print(f"Found footer elements in procrm: {p}")

# 3. Check ezconsultants
ezcon_dir = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/src"
for root, _, files in os.walk(ezcon_dir):
    for f in files:
        if f.endswith(('.jsx', '.js', '.tsx', '.ts')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as file:
                content = file.read()
            if 'Privacy Policy' in content or '© 2026 EZ Consultants' in content:
                print(f"Found footer elements in ezconsultants: {p}")

# 4. Check ezmortgagebroker
ezm_dir = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
for f in os.listdir(ezm_dir):
    if f.endswith('.html'):
        p = os.path.join(ezm_dir, f)
        with open(p, 'r', encoding='utf-8') as file:
            content = file.read()
        if 'Privacy Policy' in content:
            print(f"Found footer in ezmortgagebroker: {p}")

# 5. Check finnova
fin_dir = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
for f in os.listdir(fin_dir):
    if f.endswith('.html'):
        p = os.path.join(fin_dir, f)
        with open(p, 'r', encoding='utf-8') as file:
            content = file.read()
        if 'Privacy Policy' in content or 'footer' in content:
            print(f"Found footer in Finnova: {p}")
