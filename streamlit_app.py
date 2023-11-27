#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Data URL for loading the dataset
DATA_URL = 'https://raw.githubusercontent.com/JesHP73/IntersectionalClimateLense/82562b5a84f5af80373d79691b331ed0c33843ea/data_sets/socio_economical_agg_dataset.csv'

# Function to load data - cached to improve performance
@st.cache
def load_data():
    # I'm loading the data from the specified URL
    data = pd.read_csv(DATA_URL)
    # Renaming columns to lowercase for consistency
    data.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    # Converting the date column to datetime format, assuming 'decade' is the date column
    data['decade'] = pd.to_datetime(data['decade'])
    return data

# Load the data and store it in 'combined_data'
combined_data = load_data()

# Set up the page configuration
st.set_page_config(page_title="Intersectional Climate Lense Open Source", layout="wide")

# Define a function to plot GNI vs AQI
def plot_gni_vs_aqi(df, selected_region, selected_decade):
    # Filtering data based on the selected region and decade
    filtered_data = df[(df['region'].isin(selected_region)) & (df['decade'].isin(selected_decade))]
    # Creating a scatter plot
    fig, ax = plt.subplots()
    sns.scatterplot(x='avg_gni_ppp', y='avg_aqi_index', hue='region', data=filtered_data, ax=ax)
    st.pyplot(fig)

# Define a function to plot trends over time
def plot_trends_over_time(df, selected_metric):
    # Creating a line plot for the selected metric over time
    fig, ax = plt.subplots()
    sns.lineplot(x='decade', y=selected_metric, hue='region', data=df, ax=ax)
    st.pyplot(fig)

# Main title of the app
st.title('Intersectional Climate Open Source')
st.write('Trends in Air Quality and Economic Development Over Time')

# Set up sidebar filters
# I'm allowing users to select different options to filter the data
selected_region = st.sidebar.multiselect('Select Region', options=combined_data['region'].unique())
selected_decade = st.sidebar.multiselect('Select Decade', options=combined_data['decade'].unique())
selected_metric = st.sidebar.selectbox('Select Metric', options=['avg_aqi_index', 'avg_gni_ppp', 'total_population'])

# Displaying the plots based on selected filters
# Plot for trends over time
plot_trends_over_time(combined_data, selected_metric)

# Tabs for different analyses
tab1, tab2 = st.tabs(["GNI vs AQI Analysis", "Trends Over Time"])

with tab1:
    st.header("Income Group vs AQI Analysis")
    st.write("Visualize how Gross National Income correlates with Air Quality.")
    plot_gni_vs_aqi(combined_data, selected_region, selected_decade)

with tab2:
    st.header("Trends in Air Quality and Economic Development Over Time")
    plot_trends_over_time(combined_data, selected_metric)

# Function to convert DataFrame to CSV for download
@st.cache
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Code for downloading filtered data as CSV
csv = convert_df_to_csv(combined_data)  # Convert the filtered data to CSV
st.download_button(label="Download data as CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')

# Feedback section for user input
st.text_area("Feedback", "Enter your feedback here")
st.button("Submit")

