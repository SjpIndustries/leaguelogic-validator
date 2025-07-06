import streamlit as st
from datetime import datetime, timedelta
import pytz
import hashlib

st.set_page_config(page_title="LeagueLogic ∞VMAX T-Minus Validator — GODMODE", layout="centered")

st.title("🏁 LeagueLogic ∞VMAX T-minus Validator — GODMODE")
st.markdown("#### Elite Tactical Compliance Tool for $10M-Tier Executions")

# Input fields
kickoff_time = st.time_input("Kickoff Time (AEST)", value=datetime.strptime("20:00", "%H:%M").time())
execution_time = st.time_input("Execution Time (AEST)", value=datetime.now(pytz.timezone("Australia/Brisbane")).time())

# T-minus calculation
today = datetime.now(pytz.timezone("Australia/Brisbane")).date()
kickoff_dt = datetime.combine(today, kickoff_time).replace(tzinfo=pytz.timezone("Australia/Brisbane"))
execution_dt = datetime.combine(today, execution_time).replace(tzinfo=pytz.timezone("Australia/Brisbane"))
t_minus = int((kickoff_dt - execution_dt).total_seconds() / 60)

# Validator
if t_minus > 90:
    status = "⛔ Too Early — Execution DISQUALIFIED"
elif 30 <= t_minus <= 90:
    if t_minus == 33:
        status = "✅ Optimal Timing — T-33 EXECUTION LOCKED"
    else:
        status = "✅ Valid Timing — Within T-90 to T-30 Window"
elif t_minus < 30 and t_minus >= 0:
    status = "⚠️ Late Execution — Accuracy At Risk"
else:
    status = "❌ Execution After Kickoff — DISQUALIFIED"

# SHA-3 Execution Hash
timestamp_str = execution_dt.strftime("%Y%m%d%H%M%S%Z")
hash_input = f"LeagueLogic_EXEC_{timestamp_str}"
execution_hash = hashlib.sha3_256(hash_input.encode()).hexdigest()

# Display results
st.markdown(f"### 🕒 T-minus: T-{abs(t_minus)} minutes")
st.markdown(f"### 🔐 Execution Status: {status}")
st.markdown(f"### 🔑 SHA-3 Hash: `{execution_hash}`")
