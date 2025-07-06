
import streamlit as st
import pandas as pd
import pytz
from datetime import datetime
import hashlib

st.set_page_config(page_title="LeagueLogic ∞VMAX T-minus Validator — GODMODE", layout="centered")

st.title("🏁 LeagueLogic ∞VMAX T-minus Validator — GODMODE")
st.markdown("#### Elite Tactical Compliance Tool for $10M-Tier Executions")
st.markdown("---")

@st.cache_data
def load_fixtures():
    sheet_url = "https://docs.google.com/spreadsheets/d/1wdUvnbFeDrHl5sD3Y5HuzH-j3yIXIUTW0JAMJZ0Ly2c/export?format=csv&gid=279341718"
    df = pd.read_csv(sheet_url)
    df = df[df['KICK-OFF AEST'].notna()]
    df['Parsed Kickoff'] = pd.to_datetime(df['KICK-OFF AEST'], format='%H:%M').dt.time
    return df

df = load_fixtures()

# Filter only unplayed (non-color coded) matches
upcoming_fixtures = df[df['Fixture'].notna()].reset_index(drop=True)

# Dropdown
selected_index = st.selectbox("Select Upcoming Fixture", upcoming_fixtures.index, format_func=lambda i: f"{upcoming_fixtures.loc[i, 'Fixture']} — {upcoming_fixtures.loc[i, 'Date']} @ {upcoming_fixtures.loc[i, 'Venue']}")

fixture_row = upcoming_fixtures.loc[selected_index]
fixture = fixture_row['Fixture']
venue = fixture_row['Venue']
date = fixture_row['Date']
kickoff_time = fixture_row['Parsed Kickoff']

st.markdown(f"### 📅 {fixture} — {date}")
st.markdown(f"**🏟 Venue:** {venue}")
st.markdown(f"**⏰ Kickoff (AEST):** {kickoff_time.strftime('%H:%M')}")
st.markdown("---")

# Execution time input
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
hash_input = f"{fixture}_{timestamp_str}"
execution_hash = hashlib.sha3_256(hash_input.encode()).hexdigest()

# Display results
st.markdown(f"### 🕒 T-minus: T-{abs(t_minus)} minutes")
st.markdown(f"### 🔐 Execution Status: {status}")
st.markdown(f"### 🔑 SHA-3 Hash: `{execution_hash}`")
