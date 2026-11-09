
RELEVANCE_PROMPT = """
You are a content relevance analyst for CryptoPulse AI,
a cryptography and fintech intelligence newsletter.

Evaluate the following article.

TITLE:
{title}

DESCRIPTION:
{description}

SOURCE:
{source}

Our newsletter focuses on:

1. CRYPTOGRAPHY
   - Post-quantum cryptography
   - Zero-knowledge proofs
   - Homomorphic encryption
   - Multi-party computation
   - Digital signatures
   - Cryptographic protocols

2. PAYMENT SECURITY
   - UPI security
   - Payment tokenization
   - Transaction security
   - Secure authentication
   - Payment fraud prevention

3. FINTECH REGULATION
   - NPCI announcements
   - RBI circulars
   - Digital payment regulations
   - Financial data protection

4. CYBERSECURITY
   - Cryptographic vulnerabilities
   - Security advisories
   - Encryption attacks
   - Financial data breaches

Evaluate the article on a scale of 0 to 100.

Scoring guidance:
- 90-100: Directly relevant and highly significant.
- 70-89: Strong relevance to our audience.
- 60-69: Moderately relevant.
- 30-59: Weak or indirect relevance.
- 0-29: Not relevant.

Return ONLY valid JSON in this format:

{{
    "relevance_score": 85,
    "category": "cryptography",
    "reason": "Brief explanation of relevance"
}}

Allowed categories:
cryptography, payment_security,
fintech_regulation, cybersecurity

IMPORTANT:
- Do not invent information.
- Base the score on the supplied article.
- Do not consider an article relevant merely because it
  mentions technology or finance.
"""
