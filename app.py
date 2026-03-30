import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Study Planner", layout="centered")

# Quotes
quotes = [
    "Discipline beats motivation.",
    "Stay consistent, success will follow.",
    "Focus now, relax later.",
    "Dream big, start small.",
    "You are closer than you think."
]

st.title("📚 Smart Study Planner")
st.write(random.choice(quotes))

# Session data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Subject", "Hours", "Marks"])

if "stars" not in st.session_state:
    st.session_state.stars = 0

# Input
st.header("➕ Add Study Data")
subject = st.text_input("Subject")
hours = st.number_input("Study Hours", 0.0)
marks = st.number_input("Marks", 0)

if st.button("Add"):
    new = pd.DataFrame([[subject, hours, marks]],
                       columns=["Subject", "Hours", "Marks"])
    st.session_state.data = pd.concat([st.session_state.data, new], ignore_index=True)
    st.success("Added!")

# Show data
st.header("📊 Data")
st.dataframe(st.session_state.data)

# Weak subject
if not st.session_state.data.empty:
    avg = st.session_state.data.groupby("Subject")["Marks"].mean()
    weak = avg.idxmin()
    st.warning(f"Focus more on: {weak}")

# Timetable
st.header("📅 Timetable")
if not st.session_state.data.empty:
    for sub in st.session_state.data["Subject"].unique():
        if sub == weak:
            st.write(f"{sub}: 2 hours")
        else:
            st.write(f"{sub}: 1 hour")

# Reward
st.header("⭐ Rewards")
if st.button("Complete Study"):
    st.session_state.stars += 1
    st.success("You earned a star!")

st.write(f"Total Stars: {st.session_state.stars}")

# Chart
st.header("📈 Study Hours")
if not st.session_state.data.empty:
    st.bar_chart(st.session_state.data.groupby("Subject")["Hours"].sum())
