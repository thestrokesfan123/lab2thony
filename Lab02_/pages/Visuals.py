# This creates the page for displaying data visualizations.
import streamlit as st
from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
infile = open(Path(__file__).parent / "mydata.json")
myData = json.load(infile)

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json

st.subheader(myData["chart_title"])
chartData = pd.DataFrame(myData["data_points"])
st.area_chart(chartData, x="label", y="value")

#dynamic/advanced

st.subheader("Dynamic Data Visualization")

if "num_items" not in st.session_state:
    st.session_state.num_items = len(myData["data_points"])

st.session_state.num_items = st.slider(
    "Number of items to display",
    min_value=1,
    max_value=len(myData["data_points"]),
    value=st.session_state.num_items
)

chartData = pd.DataFrame(myData["data_points"])
displayData = chartData.head(st.session_state.num_items)

fig, ax = plt.subplots()
ax.bar(displayData["label"], displayData["value"])

ax.set_title("Values by Item")
ax.set_xlabel("Item")
ax.set_ylabel("Value")

st.pyplot(fig)


# PART 2: GRAPHS FROM data.csv
csv_file = Path(__file__).parent / "data.csv"

st.subheader("Survey Data")

if csv_file.exists() and csv_file.stat().st_size > 0:
    csvData = pd.read_csv(csv_file)
    csvData["Value"] = pd.to_numeric(csvData["Value"], errors="coerce")
    csvData = csvData.dropna(subset=["Category", "Value"])

    if not csvData.empty:
        # static
        st.subheader("Static Survey Data")
        st.bar_chart(csvData, x="Category", y="Value")

        # dynamic
        st.subheader("Dynamic Survey Data")

        if "csv_num_items" not in st.session_state:
            st.session_state.csv_num_items = len(csvData)

        st.session_state.csv_num_items = st.slider(
            "Number of survey entries to display",
            min_value=1,
            max_value=len(csvData),
            value=min(st.session_state.csv_num_items, len(csvData)),
            key="csv_num_items_slider"
        )

        displayCSV = csvData.head(st.session_state.csv_num_items)

        fig, ax = plt.subplots()
        ax.scatter(displayCSV["Category"], displayCSV["Value"])

        ax.set_title("Survey Values by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Value")
        plt.xticks(rotation=45)

        st.pyplot(fig)
    else:
        st.warning("The CSV file does not contain valid numeric values.")
else:
    st.warning("No survey data has been collected yet. Submit responses on the Survey page first.")
