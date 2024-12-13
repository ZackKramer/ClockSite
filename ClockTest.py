import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.title("Clock Time")

studf = pd.read_csv('stulist.csv')

name = st.selectbox('Your Name', options = studf['Name'])

FILE_PATH = "shared_data.csv"

# Load the shared dataframe from CSV
if os.path.exists(FILE_PATH):
    dataframe = pd.read_csv(FILE_PATH)
    dataframe['Clock In'] = pd.to_datetime(dataframe['Clock In'])
    dataframe['Clock Out'] = pd.to_datetime(dataframe['Clock Out'])
else:
    dataframe = pd.DataFrame(columns=['Name', 'Clock In', 'Clock Out', 'Hours Worked'])

# Function to save the dataframe to a file
def save_to_csv(df):
    df.to_csv(FILE_PATH, index=False)

st.title("Clock In/Out System")

# Text input for user's name
name = st.text_input("Enter your name:")

# Button to clock in
if st.button("Clock In"):
    if name.strip():
        current_datetime = datetime.now()
        new_row = {'Name': name, 'Clock In': current_datetime, 'Clock Out': None, 'Hours Worked': None}
        dataframe = pd.concat([dataframe, pd.DataFrame([new_row])], ignore_index=True)
        save_to_csv(dataframe)
        st.success("Clocked in successfully!")
    else:
        st.error("Please enter a valid name.")

# Button to clock out
if st.button("Clock Out"):
    if name.strip():
        mask = (dataframe['Name'] == name) & (dataframe['Clock Out'].isna())
        if mask.any():
            current_datetime = datetime.now()
            row_index = mask.idxmax()
            dataframe.loc[row_index, 'Clock Out'] = current_datetime
            clock_in_time = dataframe.loc[row_index, 'Clock In']
            hours_worked = (current_datetime - clock_in_time).total_seconds() / 3600
            dataframe.loc[row_index, 'Hours Worked'] = round(hours_worked, 2)
            save_to_csv(dataframe)
            st.success("Clocked out successfully!")
        else:
            st.warning("No active clock-in record found for this name.")
    else:
        st.error("Please enter a valid name.")

# Display the updated dataframe
st.write("Current DataFrame:", dataframe)

# Button to export and clear
if st.button("Export DataFrame and Clear"):
    if not dataframe.empty:
        csv = dataframe.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="time_tracking.csv", mime="text/csv")
        dataframe = pd.DataFrame(columns=['Name', 'Clock In', 'Clock Out', 'Hours Worked'])
        save_to_csv(dataframe)
        st.success("Dataframe exported and cleared!")
    else:
        st.warning("Dataframe is empty. Nothing to export.")