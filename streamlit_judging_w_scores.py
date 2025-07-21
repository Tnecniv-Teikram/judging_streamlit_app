import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

# Load team data
TEAMS = [
    {"id": 1, "name": "MOD"},
    {"id": 2, "name": "Aerial AI"},
    {"id": 3, "name": "Sard"},
    {"id": 4, "name": "Land safer"},
    {"id": 5, "name": "MarEye"},
    {"id": 6, "name": "Rashed's team"},
    {"id": 7, "name": "mahra aldhaheri"},
    {"id": 8, "name": "Pave Patrol"},
    {"id": 9, "name": "GeoPV"},
    {"id": 10, "name": "Asmaa team"},
    {"id": 11, "name": "Ghaf Root"},
    {"id": 12, "name": "GeoResQ"},
    {"id": 13, "name": "Flood Sentinels"},
    {"id": 14, "name": "DoubleA"},
    {"id": 15, "name": "TBD"}
]

# Define criteria weights
CRITERIA_WEIGHTS = {
    "problem_definition": 15,
    "technical_execution": 20,
    "results_interpretation": 20,
    "learning_reflection": 10,
    "presentation_quality": 15,
    "long_term_vision": 15,
    "scientific_evaluation": 10,
    "team_expertise": 10
}

# Function to calculate weighted score
def calculate_weighted_score(scores, criteria_weights):
    total_score = 0
    for criterion_id, weight in criteria_weights.items():
        if criterion_id in scores:
            total_score += scores[criterion_id] * weight / 100
    return total_score

# Collect all session files
session_files = [f for f in os.listdir('.') if f.startswith('session_') and f.endswith('.json')]

# Aggregate scores and judge counts
team_scores = {team['id']: [] for team in TEAMS}
judge_counts = {team['id']: 0 for team in TEAMS}

for file in session_files:
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        for team in TEAMS:
            team_key = f"team_{team['id']}"
            if team_key in data:
                team_scores[team['id']].append(calculate_weighted_score(data[team_key], CRITERIA_WEIGHTS))
                judge_counts[team['id']] += 1
    except Exception:
        continue

# Compute average and total scores
avg_scores = {team_id: (sum(scores) / len(scores) if scores else 0) for team_id, scores in team_scores.items()}
total_scores = {team_id: sum(scores) for team_id, scores in team_scores.items()}

# Prepare data for display
summary_data = []
for team in TEAMS:
    tid = team['id']
    summary_data.append({
        "Team": team['name'],
        "Total Score": round(total_scores[tid], 2),
        "Average Score": round(avg_scores[tid], 2),
        "Number of Judges": judge_counts[tid]
    })

df_summary = pd.DataFrame(summary_data).sort_values(by="Total Score", ascending=False)

# Streamlit UI
st.set_page_config(page_title="Judging Dashboard", layout="wide")
st.title("📈 Live Scores Dashboard")

tab1, tab2 = st.tabs(["📊 Score Table", "📉 Score Comparison Chart"])

with tab1:
    st.subheader("Live Scores by Team")
    st.dataframe(df_summary, use_container_width=True)

with tab2:
    st.subheader("Total Score Comparison")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df_summary["Team"], df_summary["Total Score"], color='cornflowerblue')
    ax.set_xlabel("Total Score")
    ax.set_title("Total Scores by Team")
    plt.tight_layout()
    st.pyplot(fig)

