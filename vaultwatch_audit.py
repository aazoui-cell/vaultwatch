import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")
MODEL = "nvidia/Qwen3.6-35B-A3B-NVFP4"

RULES = """Restricted Deals: ACME (Project Titan), GLOBEX (Project Apex).
Prohibited: 1) Trading restricted tickers, 2) Exfiltrating customer PII/SSNs to personal email, 3) Order book spoofing."""

EVENTS = [
    "Dave Vance (Equities): Advisory briefed us on Project Titan. Bought 25k OTM ACME calls across three accounts. Keep quiet.",
    "Sarah Lin (Fixed Income): Routine quarterly portfolio duration rebalance on US 10Y Treasuries executed within tracking error.",
    "Marcus Brody (Wealth): Sent VIP client master list with unmasked SSNs and routing numbers to personal-backup@gmail.com.",
    "Elena Rostova (Derivatives): Laddering 500k fake buy bids on $ZETA to push midpoint up, canceling before execution."
]

print("\n" + "="*70 + "\n  VAULTWATCH: LOCAL AIR-GAPPED SURVEILLANCE (DELL GB10)\n" + "="*70)

for ev in EVENTS:
    print(f"\n[INGESTING LOG] {ev}")
    prompt = f"Rules: {RULES}\nEvent: {ev}\nTask: Determine if this violates bank compliance. Output status (🚨 FLAGGED or ✅ COMPLIANT), Category, Rule, and 1-sentence Explanation."
    res = client.chat.completions.create(
        model=MODEL,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    )
    print("AUDIT VERDICT:\n" + res.choices[0].message.content.strip())
    print("-" * 70)
