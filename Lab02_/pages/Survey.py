# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
from pathlib import Path

csv_file = Path(__file__).parent / "data.csv"

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

with st.form("survey_form"):
    category_input = st.text_input("Enter a category:")
    value_input = st.text_input("Enter a corresponding value:")
    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if category_input.strip() == "":
            st.error("Please enter a category.")
        else:
            try:
                value = float(value_input)
                new_data = pd.DataFrame({
                    "Category": [category_input],
                    "Value": [value]
                })
                new_data.to_csv(
                    csv_file,
                    mode="a",
                    header=not csv_file.exists() or csv_file.stat().st_size == 0,
                    index=False
                )
                st.success("Your data has been submitted!")
                st.write(f"You entered: **Category:** {category_input}, **Value:** {value}")
            except ValueError:
                st.error("Please enter a numeric value.")

st.divider()
st.header("Current Data in CSV")

if csv_file.exists() and csv_file.stat().st_size > 0:
    current_data_df = pd.read_csv(csv_file)
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")

