import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")
MODEL = "nvidia/Qwen3.6-35B-A3B-NVFP4"

app = App(token=os.environ["SLACK_BOT_TOKEN"])

RULES = """Restricted Deals: ACME (Project Titan), GLOBEX (Project Apex).
Prohibited: 1) Trading restricted tickers, 2) Exfiltrating customer PII/SSNs to personal email, 3) Order book spoofing."""

def audit_event(text: str) -> str:
    prompt = f"""You are VaultWatch, an on-premise air-gapped Bank Compliance Surveillance Agent running locally on Dell GB10.
Rules:
{RULES}

Event to Audit:
"{text}"

Task: Determine if this violates bank compliance.
Output strictly:
- Status: 🚨 FLAGGED or ✅ COMPLIANT
- Category: (Insider Trading, PII Exfiltration, Spoofing, or Benign)
- Rule: (Policy violated or None)
- Explanation: (1 concise sentence)"""

    res = client.chat.completions.create(
        model=MODEL,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content.strip()

@app.event("app_mention")
def handle_mention(event, say):
    text = event.get("text", "")
    clean = text.split(">", 1)[-1].strip() if ">" in text else text
    say("🔍 *VaultWatch GB10 Surveillance Agent* analyzing payload...")
    say(f"```\n{audit_event(clean)}\n```")

@app.message("")
def handle_message(message, say):
    text = message.get("text", "").strip()
    if text.startswith("!audit "):
        payload = text.replace("!audit ", "").strip()
        say("🔍 *VaultWatch GB10 Surveillance Agent* analyzing payload...")
        say(f"```\n{audit_event(payload)}\n```")

if __name__ == "__main__":
    print("⚡ VaultWatch Slack Bot live via Socket Mode (Local vLLM backend)...")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
