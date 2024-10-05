import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
bike_df = pd.read_csv("dashboard/bike_data.csv")

# Convert 'date_day' to datetime
bike_df['date_day'] = pd.to_datetime(bike_df['date_day'])

# Sidebar for filtering
st.sidebar.header('Filter Data')
start_date = st.sidebar.date_input("Start Date", bike_df['date_day'].min())
end_date = st.sidebar.date_input("End Date", bike_df['date_day'].max())

# Filter data based on date input
filtered_data = bike_df[(bike_df['date_day'] >= pd.to_datetime(start_date)) & (bike_df['date_day'] <= pd.to_datetime(end_date))]

# Main Page
st.title("Bike Sharing Dashboard")

# Visual 1: daily rental trend
st.subheader("Daily Rental Trend")

# Detail total
col1, col2, col3 = st.columns(3)
with col1:
  total_user = filtered_data.total_user.sum()
  st.metric("Total User", value=total_user)
 
with col2:
  casual_user = filtered_data.casual_user.sum()
  st.metric("Casual/Not registered", value=casual_user)
with col3:
  registered_user = filtered_data.registered_user.sum()
  st.metric("Registered", value=registered_user)

# Line chart
daily_trend = filtered_data.groupby('date_day')['total_user'].sum()
st.line_chart(daily_trend)

# Visual 2: Hourly rental distribution
st.subheader("Hourly Rental Distribution")
hourly_trend = filtered_data.groupby('hour')['total_user'].sum()
st.bar_chart(hourly_trend)

# Visual 3: Bar chart for rentals by weather condition
st.subheader("Rentals by Weather Condition")
weather_rentals = filtered_data.groupby('weathersit')['total_user'].sum().reset_index()

fig, ax = plt.subplots()
sns.barplot(data=weather_rentals, x='weathersit', y='total_user', ax=ax)
ax.set_title("Total Rentals by Weather Condition")
st.pyplot(fig)

# Visual 3: Bar chart for rentals by holiday
st.subheader("Rentals on Holiday")
weather_rentals = filtered_data.groupby('holiday')['total_user'].sum().reset_index()

fig, ax = plt.subplots()
sns.barplot(data=weather_rentals, x='holiday', y='total_user', ax=ax)
ax.set_title("Total Rentals by Weather Condition")
st.pyplot(fig)


# Additional filtering options
st.sidebar.subheader("Additional Filters")
selected_weather = st.sidebar.multiselect("Select Weather Conditions", options=['Clear', 'Cloudy', 'Light Rain/Snow', 'Heavy Rain/Snow'], default=['Clear', 'Cloudy', 'Light Rain/Snow', 'Heavy Rain/Snow'])
filtered_data = filtered_data[filtered_data['weathersit'].isin(selected_weather)]
