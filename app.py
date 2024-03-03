import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

st.title("Analisis Kualitas Udara di Beijing")
combined_data = pd.read_csv('data/concated_df.csv')
categoric_data = pd.read_csv('data/categoric_combined_df.csv')

combined_data['datetime'] = pd.to_datetime(combined_data['datetime'])

#For sidebar 
selected_station = st.sidebar.multiselect(
    'Select Station', 
    options=['All stations']+list(combined_data['station'].unique()),
    default=['All stations']
    )

start_date = st.sidebar.date_input('Start Date', min(combined_data['datetime']).date(),
                                   min_value=pd.to_datetime('2013-03-01').date(),
                                   max_value=pd.to_datetime('2017-02-28').date())
end_date = st.sidebar.date_input('End Date', max(combined_data['datetime']).date(),
                                 min_value=pd.to_datetime('2013-03-01').date(),
                                 max_value=pd.to_datetime('2017-02-28').date())

start_datetime = pd.to_datetime(start_date).date
end_datetime = pd.to_datetime(end_date).date
combined_data['date'] = combined_data['datetime'].dt.date
combined_data['hour'] = combined_data['datetime'].dt.hour



## Filter the multiselect
if 'All Station' in selected_station:
    selected_station.remove('All Station')

if not selected_station:
    filtered_data = combined_data[(combined_data['date'] >= start_datetime() and combined_data['date'] <= end_datetime())]
elif 'All Station' in selected_station:
    filtered_data = combined_data[(combined_data['date'] >= start_datetime() and combined_data['date'] <= end_datetime())]
else:
    filtered_data = combined_data[(combined_data['station'].isin(selected_station)) &
                                (combined_data['date'] >= start_datetime()) & (combined_data['date'] <= end_datetime())]




category_count = combined_data['Category'].value_counts().reset_index()
category_count.columns = ['Category', 'Count']
category_count['Category'] = pd.Categorical(category_count['Category'], ordered=True)
#print(category_counts)
category_count= category_count.sort_values('Category')

# Chart for each polutant
factors = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO']
col1, col2 = st.columns(2)
# For the left selectbox
with col1:
    selected_factor = st.selectbox('Select Polutant Factor', options=factors)

# For the right selectbox
with col2:
    selected_freq = st.selectbox('Select the Frequency', options=['Weekly', 'Monthly', 'Yearly'])
    
#print(selected_freq)
    
data_resample = filtered_data.groupby(['station', pd.Grouper(key='datetime', freq=selected_freq[0])])[selected_factor].mean().reset_index()

fig = px.line(data_resample, x='datetime', y=selected_factor, color='station',
              title=f'{selected_factor} {selected_freq} Levels by Station Over Time')
st.plotly_chart(fig)

# For Piechart
fig = px.pie(category_count, values='Count', names='Category', title='Air Quality Categories Percentage')
st.plotly_chart(fig)



# STYLING
hide_st_style = """
            <style>
            #MainMenu {visibility:hidden}
            footer {visibility:hidden}
            header {visibility:hidden}
            </style>
            """
            
st.markdown(hide_st_style, unsafe_allow_html=True)
