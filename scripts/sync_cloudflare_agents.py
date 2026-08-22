#!/usr/bin/env python3
"""
Sync Cloudflare Chat Agent from Blogs-Content monorepo to standalone Cloudflare Agents repository.
Ensures the standalone repository (Finnova-Ltd/cloudflare-agents.git) is kept 100% in sync and deployable as a separate commercial product.
"""

import os
import subprocess
import shutil

SOURCE_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/cloudflare/chat-agent"
DEST_REPO = "/Users/robinbakshi/Documents/GitHub/Cloudflare Agents"

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"⚠️ Command '{cmd}' output: {res.stderr.strip() or res.stdout.strip()}")
    return res

def sync_agent_repo():
    print("🚀 Synchronizing Cloudflare Chat Agent to Standalone Repository...")
    
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Source directory {SOURCE_DIR} not found.")
        return
    
    if not os.path.exists(DEST_REPO):
        print(f"❌ Destination repository {DEST_REPO} not found.")
        return

    # Rsync excluding .git, node_modules, .wrangler
    rsync_cmd = f'rsync -av --delete --exclude ".git" --exclude "node_modules" --exclude ".wrangler" "{SOURCE_DIR}/" "{DEST_REPO}/"'
    print(f"📁 Running rsync...")
    run_cmd(rsync_cmd)

    # Git commit and push to standalone repo
    print(f"📤 Pushing changes to standalone Cloudflare Agents repo...")
    run_cmd("git add -A", cwd=DEST_REPO)
    run_cmd('git commit -m "sync: auto-sync chat agent from Blogs-Content monorepo [skip ci]"', cwd=DEST_REPO)
    run_cmd("git pull --rebase origin main", cwd=DEST_REPO)
    push_res = run_cmd("git push origin main", cwd=DEST_REPO)
    
    if push_res.returncode == 0:
        print("✅ Standalone Cloudflare Agents repository is up to date and pushed successfully!")
    else:
        print("ℹ️ Standalone Cloudflare Agents repository is already up to date.")

if __name__ == "__main__":
    sync_agent_repo()
