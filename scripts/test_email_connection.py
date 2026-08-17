#!/usr/bin/env python3
"""
EZ Mortgage Broker - Email & IMAP/SMTP Connection Diagnostic Tester
Tests live SSL handshake and authentication for Axigen / HostYourServices.
"""

import imaplib
import smtplib
import ssl
import os
import sys

def test_imap(host, port, username, password):
    print(f"\n📡 Testing IMAP Connection -> {host}:{port} (SSL)...")
    try:
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(host, port, ssl_context=context)
        mail.login(username, password)
        status, folder_list = mail.list()
        print(f"  ✅ IMAP Login Successful for {username}!")
        print(f"  📁 Available Folders: {len(folder_list)} mailboxes detected.")
        mail.logout()
        return True
    except Exception as e:
        print(f"  ❌ IMAP Connection Failed: {e}")
        return False

def test_smtp(host, port, username, password):
    print(f"\n📤 Testing SMTP Connection -> {host}:{port} (SSL)...")
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context, timeout=10) as server:
            server.login(username, password)
            print(f"  ✅ SMTP Login & Handshake Successful for {username}!")
            return True
    except Exception as e:
        print(f"  ❌ SMTP SSL (Port 465) Failed: {e}")
        # Try TLS on 587
        print(f"  🔄 Attempting fallback STARTTLS on port 587...")
        try:
            with smtplib.SMTP(host, 587, timeout=10) as server:
                server.starttls(context=context)
                server.login(username, password)
                print(f"  ✅ SMTP STARTTLS (Port 587) Successful!")
                return True
        except Exception as e2:
            print(f"  ❌ SMTP 587 Fallback Failed: {e2}")
            return False

if __name__ == "__main__":
    imap_host = os.environ.get("IMAP_HOST", "syn08ae.syd5.hostyourservices.net")
    imap_port = int(os.environ.get("IMAP_PORT", 993))
    smtp_host = os.environ.get("SMTP_HOST", "ax.email")
    smtp_port = int(os.environ.get("SMTP_PORT", 465))
    user = os.environ.get("IMAP_USERNAME", "info@ezmortgagebroker.com.au")
    pwd = os.environ.get("IMAP_PASSWORD", "G00dd@Y20262027")

    print("==================================================")
    print("EZ MORTGAGE BROKER - MAIL SERVER DIAGNOSTIC TEST")
    print("==================================================")
    print(f"Account: {user}")

    imap_ok = test_imap(imap_host, imap_port, user, pwd)
    smtp_ok = test_smtp(smtp_host, smtp_port, user, pwd)

    if not smtp_ok and smtp_host != imap_host:
        print(f"\n🔄 Testing alternative SMTP host: {imap_host}...")
        test_smtp(imap_host, 465, user, pwd)

    print("\n==================================================")
    print(f"RESULT: IMAP = {'🟢 PASS' if imap_ok else '🔴 FAIL'} | SMTP = {'🟢 PASS' if smtp_ok else '🔴 FAIL'}")
    print("==================================================")
