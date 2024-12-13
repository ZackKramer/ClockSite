import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.title("Clock Time")

studf = pd.read_csv('stulist.csv')

name = st.selectbox('Your Name', options = studf['Name'])

# Button to clock in
if st.button("Clock In"):
    if name.strip():  # Ensure the name is not empty
        # Get the current date and time
        current_datetime = datetime.now()
        
        # Add a new row with Clock In timestamp
        new_row = {'Name': name, 'Clock In': current_datetime, 'Clock Out': None, 'Hours Worked': None}
        st.session_state['dataframe'] = pd.concat([
            st.session_state['dataframe'],
            pd.DataFrame([new_row])
        ], ignore_index=True)
    else:
        st.error("Please enter a valid name.")

# Button to clock out
if st.button("Clock Out"):
    if name.strip():  # Ensure the name is not empty
        # Find the last row for the given name without a Clock Out timestamp
        df = st.session_state['dataframe']
        mask = (df['Name'] == name) & (df['Clock Out'].isna())
        if mask.any():
            current_datetime = datetime.now()
            # Update the Clock Out column for the last Clock In row
            row_index = mask.idxmax()
            st.session_state['dataframe'].loc[row_index, 'Clock Out'] = current_datetime
            
            # Calculate hours worked
            clock_in_time = st.session_state['dataframe'].loc[row_index, 'Clock In']
            hours_worked = (current_datetime - clock_in_time).total_seconds() / 3600
            st.session_state['dataframe'].loc[row_index, 'Hours Worked'] = round(hours_worked, 2)
        else:
            st.warning("No active clock-in record found for this name.")
    else:
        st.error("Please enter a valid name.")

# Display the updated dataframe
st.write("Current DataFrame:", st.session_state['dataframe'])

# Button to export the dataframe as a CSV and clear it
if st.button("Export DataFrame and Clear"):
    if not st.session_state['dataframe'].empty:
        # Add a Date column with only the date part
        dataframe_with_date = st.session_state['dataframe'].copy()
        dataframe_with_date['Date'] = dataframe_with_date['Clock In'].dt.date
        
        # Export to CSV
        csv = dataframe_with_date.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="time_tracking.csv", mime="text/csv")
        
        # Clear the dataframe
        st.session_state['dataframe'] = pd.DataFrame(columns=['Name', 'Clock In', 'Clock Out', 'Hours Worked'])
        st.success("Dataframe exported and cleared!")
    else:
        st.warning("Dataframe is empty. Nothing to export.")
