
import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_autorefresh import st_autorefresh

from config import LIBRARY_CAPACITY, REFRESH_INTERVAL
from queuewise.database import create_table, get_readings
from queuewise.data_source import load_demo_data
from queuewise.occupancy import classify_crowd
from queuewise.analytics import find_less_crowded_hours


# Page settings
st.set_page_config(
    page_title="QueueWise",
    page_icon="📚",
    layout="wide"
)

# Refresh dashboard every 30 seconds
st_autorefresh(
    interval=REFRESH_INTERVAL,
    key="queuewise_refresh"
)

# Create database and load demo data
create_table()
load_demo_data()


# Dashboard heading
st.title("📚 QueueWise")
st.subheader("Smart Library Occupancy Monitoring System")

st.warning(
    "DEMO MODE: The displayed occupancy data is simulated, "
    "not connected to actual student ID-card scans."
)

# Retrieve data
rows = get_readings()

columns = [
    "observed_at",
    "entries",
    "exits",
    "occupancy",
    "source",
    "data_mode"
]

df = pd.DataFrame(rows, columns=columns)

if df.empty:
    st.info("No occupancy data available yet.")
    st.stop()

# Convert timestamps
df["observed_at"] = pd.to_datetime(df["observed_at"])

# Latest reading
latest = df.iloc[-1]

current_occupancy = int(latest["occupancy"])
entries = int(latest["entries"])
exits = int(latest["exits"])

crowd_level = classify_crowd(
    current_occupancy,
    LIBRARY_CAPACITY
)

occupancy_percentage = (
    current_occupancy / LIBRARY_CAPACITY
) * 100


# Occupancy summary
st.header("Current Library Status")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Occupancy",
    f"{current_occupancy} students"
)

col2.metric(
    "Entries",
    entries
)

col3.metric(
    "Exits",
    exits
)

col4.metric(
    "Crowd Level",
    crowd_level
)

st.progress(
    min(occupancy_percentage / 100, 1.0),
    text=f"Library capacity used: {occupancy_percentage:.1f}%"
)

st.caption(
    f"Last sample timestamp: "
    f"{latest['observed_at'].strftime('%d %b %Y, %I:%M %p')}"
)


# Occupancy graph
st.header("Occupancy Trend")

figure = px.line(
    df,
    x="observed_at",
    y="occupancy",
    title="Library Occupancy Over the Last 24 Sample Hours",
    labels={
        "observed_at": "Time",
        "occupancy": "Number of Students"
    },
    markers=True
)

st.plotly_chart(figure, width="stretch")

st.dataframe(df, width="stretch", hide_index=True)


# Smart Visit Time
st.header("Smart Visit Time")

less_crowded = find_less_crowded_hours(df)

if less_crowded is not None and not less_crowded.empty:

    st.write("Three least crowded sample hours:")

    for hour, average in less_crowded.items():

        formatted_hour = pd.Timestamp(
            year=2026,
            month=1,
            day=1,
            hour=int(hour)
        ).strftime("%I %p")

        st.write(
            f"🟢 {formatted_hour} — "
            f"Average occupancy: {average:.0f} students"
        )

    st.caption(
        "These are demo-based sample patterns, not reliable "
        "predictions of future occupancy."
    )


# Recent records
st.header("Recent Occupancy Records")

recent_data = df.tail(10).sort_values(
    "observed_at",
    ascending=False
)

st.dataframe(
    recent_data,
    use_container_width=True,
    hide_index=True
)


# Footer
st.divider()

st.caption(
    "QueueWise | College Project | "
    "Demo data only. Live integration requires authorised "
    "access to the college occupancy data interface."
)
