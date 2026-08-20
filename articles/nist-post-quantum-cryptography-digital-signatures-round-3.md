---
title: "NIST Advances 9 Candidates in Post-Quantum Digital Signatures (PQC Round 3): The Future of Quantum-Resistant eSignatures"
slug: "nist-pqc-digital-signatures-round-3-quantum-cryptography"
date: "2026-08-21"
author: "EZ Signature Research Team"
category: "Security & Legal Compliance"
tags:
  - "Post-Quantum Cryptography"
  - "NIST PQC"
  - "Digital Signatures"
  - "eSignatures"
  - "Cyber Security"
readTime: "6 min read"
excerpt: "NIST announces nine candidate algorithms advancing to the third round of the Additional Digital Signatures for Post-Quantum Cryptography (IR 8610). Here is how quantum-resistant cryptography protects enterprise digital contracts."
image: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80"
canonical_url: "https://ezsignature.com/blog/nist-pqc-digital-signatures-round-3-quantum-cryptography"
---

# NIST Advances 9 Candidates in Post-Quantum Digital Signatures (PQC Round 3): The Future of Quantum-Resistant eSignatures

> **Executive Summary**: The U.S. National Institute of Standards and Technology (NIST) Information Technology Laboratory has published **NIST Internal Report (IR) 8610**, announcing nine candidate algorithms advancing to the third round of the Additional Digital Signatures for the Post-Quantum Cryptography (PQC) Standardization Process. This milestone marks a critical shift for document workflows, cryptographic seals, and long-term contract enforceability.

---

## 1. The Quantum Threat to Modern Digital Signatures

Modern electronic signature architectures rely on asymmetric public-key cryptography—predominantly **RSA**, **Diffie-Hellman**, and **Elliptic Curve Digital Signature Algorithm (ECDSA)**—to generate tamper-evident seals and verify signer identity.

When cryptographically relevant quantum computers (CRQCs) become operational, Shor's algorithm will be capable of breaking these mathematical foundations in polynomial time. For digital contracts and eSignatures, this creates an urgent timeline challenge:

* **Harvest Now, Decrypt Later (HNDL)**: Malicious actors are already storing encrypted documents and signed digital envelopes.
* **Long-Term Contract Validity**: Mortgage deeds, commercial leases, NDAs, and healthcare agreements often require legal enforceability spanning **20 to 50+ years**.
* **Audit Trail Integrity**: Forensic timestamping and digital certificates must remain immutable long after quantum computing matures.

---

## 2. NIST IR 8610: The Round 3 Selection

Following extensive cryptographic review, cryptanalysis, and performance benchmarking across diverse computing architectures, NIST has selected nine candidate digital signature schemes for Round 3 evaluation:

| Algorithm Scheme | Primary Mathematical Family | Key Strengths in Document Signing |
| :--- | :--- | :--- |
| **Lattice-Based Signatures** | Module/Ring Learning With Errors | Fast verification, balanced key/signature sizes, low latency |
| **Code-Based Signatures** | Error-Correcting Codes | Strong security proofs, highly resilient mathematical structure |
| **Multivariate Signatures** | Multivariate Quadratic Polynomials | Very compact digital signature sizes, rapid verification |
| **Isogeny-Based Signatures** | Elliptic Curve Isogenies | Smallest public keys, ideal for constrained environments |
| **Stateful Hash-Based (LMS/XMSS)** | Hash-Tree Roots (SP 800-208) | Zero reliance on unproven hardness; gold standard for root certificates |

---

## 3. How EZ Signature Is Future-Proofing Electronic Signatures

To ensure complete legal enforceability under the **Australian Electronic Transactions Act 1999 (ETA)**, the **US ESIGN Act**, and international **eIDAS** standards, enterprise signature platforms must implement a proactive quantum-resilient strategy.

### The Hybrid Signature Model
EZ Signature is adopting a **Dual-Layer Hybrid Envelope Architecture**:
1. **Classical Standard Layer**: Employs industry-standard AATL (Adobe Approved Trust List) certificates with RSA-4096 / SHA-256 for backward compatibility with existing PDF readers.
2. **Post-Quantum Layer**: Integrates NIST PQC candidate algorithms to seal document integrity, timestamping, and signer biometric telemetry against future quantum decryption.

---

## 4. Key Recommendations for Business & Enterprise Leaders

1. **Audit Long-Lifecycle Documents**: Identify high-value commercial agreements that have retention requirements beyond 10 years.
2. **Transition from Legacy Hash Functions**: Ensure all document signing workflows enforce SHA-256 or SHA-3 at a minimum.
3. **Adopt Crypto-Agility**: Choose eSignature platforms designed with modular cryptographic backends capable of seamless algorithm updates.

---
*Published by EZ Signature Cryptographic Research & Compliance Division · [Read Full Technical Advisory](https://ezsignature.com/blog/nist-pqc-digital-signatures-round-3-quantum-cryptography)*
