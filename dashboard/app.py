import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Fungsi untuk memproses data
def create_day_orders_df(day_df):
    day_df['is_weekend'] = day_df['date'].dt.dayofweek >= 5  # 5 dan 6 adalah Sabtu dan Minggu
    return day_df

def create_weather_order_avg_df(day_df):
    weather_group = day_df.groupby('weather')['count'].mean().reset_index()
    return weather_group

def create_season_order_avg_df(day_df):
    season_group = day_df.groupby('season')['count'].mean().reset_index()
    return season_group

# Load cleaned data
day_data = pd.read_csv("./dashboard/cleaned_data.csv")

# Konversi kolom tanggal
day_data['date'] = pd.to_datetime(day_data['date'])
day_data.sort_values(by="date", inplace=True)
day_data.reset_index(drop=True, inplace=True)

# Filter data berdasarkan rentang waktu
min_day_date = day_data["date"].min()
max_day_date = day_data["date"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_day_date,
        max_value=max_day_date, value=[min_day_date, max_day_date]
    )

main_day_df = day_data[(day_data["date"] >= str(start_date)) & 
                    (day_data["date"] <= str(end_date))]

# Menyiapkan berbagai dataframe
day_orders_df = create_day_orders_df(main_day_df)
weather_order_avg_df = create_weather_order_avg_df(main_day_df)
season_order_avg_df = create_season_order_avg_df(main_day_df)

# Tampilan Dashboard di Streamlit
st.header('Bike Sharing Dashboard 😊')
st.markdown("---")

# Menampilkan metrik total penyewaan
col1, col2, col3 = st.columns(3)

with col1:
    total_all_type = main_day_df['count'].sum()
    st.metric("Total All Rides", value=total_all_type)

with col2:
    total_casual_type = main_day_df['casual_users'].sum()
    st.metric("Total Casual Rides", value=total_casual_type)

with col3:
    total_registered_type = main_day_df['registered_users'].sum()
    st.metric("Total Registered Rides", value=total_registered_type)


st.markdown("---")

# Visualisasi Musim
st.subheader("Pengaruh Musim terhadap Rata-rata Penyewaan Sepeda")

max_value = season_order_avg_df['count'].max()
colors = ['orange' if x == max_value else 'lightgray' for x in season_order_avg_df['count']]

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=season_order_avg_df, x='season', y='count', palette=colors, ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
st.pyplot(fig)

st.markdown("---")

# Visualisasi Cuaca
st.subheader("Pengaruh Cuaca terhadap Rata-rata Penyewaan Sepeda")

max_value = weather_order_avg_df['count'].max()
colors = ['orange' if x == max_value else 'lightgray' for x in weather_order_avg_df['count']]

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=weather_order_avg_df, x='weather', y='count', palette=colors, ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda berdasarkan Kondisi Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
st.pyplot(fig)

st.markdown("---")

# Visualisasi Weekend vs Weekday
st.subheader("Perbandingan Rata-Rata Penyewaan Sepeda: Weekend vs Weekday")

day_orders_df['day_type'] = day_orders_df['is_weekend'].replace({True: 'Weekend', False: 'Weekday'})
day_type_counts = day_orders_df.groupby('day_type')['count'].mean().reset_index()

max_value = day_type_counts['count'].max()
colors = ['orange' if x == max_value else 'lightgray' for x in day_type_counts['count']]

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=day_type_counts, x='day_type', y='count', palette=colors, ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda: Weekend vs Weekday')
ax.set_xlabel('Jenis Hari')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
st.pyplot(fig)

st.markdown("---")
