import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import timedelta

# Load the data
file_path = r'C:\Users\Asus\Music\CodeWithEhtisham\AddRover-pipeline\cleaned_data.csv'
df = pd.read_csv(file_path)

# Preprocess data
df['time'] = pd.to_datetime(df['time'])

# Sidebar filters
st.sidebar.header("🔎 Filters")
start_date = st.sidebar.date_input("Start Date", df['time'].min().date())
end_date = st.sidebar.date_input("End Date", df['time'].max().date() + timedelta(days=1))
gender_filter = st.sidebar.multiselect("Select Gender", options=df['gender'].unique(), default=df['gender'].unique())

# Filter the data
filtered_data = df[(df['time'].dt.date >= start_date) & (df['time'].dt.date <= end_date) & (df['gender'].isin(gender_filter))]

# Key metrics
total_persons = filtered_data['total_persons'].sum()
average_age = filtered_data['age'].mean()
total_men = filtered_data[filtered_data['gender'] == 'Man']['person_id'].count()
total_women = filtered_data[filtered_data['gender'] == 'Woman']['person_id'].count()
unique_ads = filtered_data['ad_id'].nunique()

# Custom CSS
st.markdown("""
    <style>
    .main-container {
        background-color: #f0f4f8;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        color: #33475b;
    }
    h1 {
        font-size: 36px;
        text-align: center;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        color: #888;
        margin-top: 50px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("🌟 Advanced Ad Performance Dashboard")

# Key Metrics Section
st.markdown("### 🚀 Key Performance Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Persons", total_persons, delta=f"{(total_persons / len(df)):.1%}")
col2.metric("Average Age", round(average_age, 1))
col3.metric("Total Men", total_men)
col4.metric("Total Women", total_women)
col5.metric("Unique Ads", unique_ads)

st.markdown("---")

# Visualization: Ad Run Time Frequency
st.markdown("### ⏱️ Ad Run Time Analysis")
ads_over_time = filtered_data['ad_id'].value_counts().reset_index()
ads_over_time.columns = ['Ad ID', 'Frequency']
run_time_chart = px.bar(
    ads_over_time,
    x='Ad ID',
    y='Frequency',
    color='Ad ID',
    title="Ad Run Time Frequency",
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(run_time_chart, use_container_width=True)

# Visualization: Gender Comparison
st.markdown("### 👥 Gender Distribution")
gender_pie = px.pie(
    filtered_data, 
    names='gender', 
    values='total_persons', 
    title="Gender Distribution",
    color_discrete_sequence=px.colors.qualitative.Safe
)
st.plotly_chart(gender_pie, use_container_width=True)

# Visualization: Age Histogram
st.markdown("### 📊 Age Distribution")
age_histogram = px.histogram(
    filtered_data, 
    x='age', 
    nbins=20, 
    title="Age Distribution by Gender", 
    color='gender',
    barmode='group',
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(age_histogram, use_container_width=True)

# Visualization: Word Cloud
st.markdown("### 🌟 Word Cloud of Ads")
feedback_text = " ".join(filtered_data['ad_id'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(feedback_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

# Visualization: Gender and Ad Interactions Heatmap
st.markdown("### 🔥 Gender and Ad Interactions (Heatmap)")
gender_ad_interaction = filtered_data.groupby(['gender', 'ad_id']).size().reset_index(name='Count')
heatmap = px.density_heatmap(
    gender_ad_interaction,
    x='ad_id',
    y='gender',
    z='Count',
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Gender and Ad Interactions",
)
st.plotly_chart(heatmap, use_container_width=True)

# Visualization: Persons Over Time (Area Chart)
st.markdown("### 📅 Persons Over Time (Area Chart)")
persons_over_time = filtered_data.groupby(filtered_data['time'].dt.date)['total_persons'].sum().reset_index()
persons_over_time.columns = ['Date', 'Total Persons']
area_chart = px.area(
    persons_over_time,
    x='Date',
    y='Total Persons',
    title="Persons Viewing Ads Over Time",
    color_discrete_sequence=['#636EFA']
)
st.plotly_chart(area_chart, use_container_width=True)

# Visualization: Ad Popularity by View Count
st.markdown("### 🏆 Ad Popularity by View Count")
ad_popularity = filtered_data.groupby('ad_id')['total_persons'].sum().reset_index()
ad_popularity.columns = ['Ad ID', 'Total Views']
popularity_chart = px.bar(
    ad_popularity.sort_values(by='Total Views', ascending=False).head(10),
    x='Ad ID',
    y='Total Views',
    title="Top 10 Most Viewed Ads",
    color='Ad ID',
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(popularity_chart, use_container_width=True)

# Visualization: Gender and Ad View Comparison
st.markdown("### 📊 Gender and Ad View Comparison")
gender_views = filtered_data.groupby('gender')['total_persons'].sum().reset_index()
gender_views_chart = px.bar(
    gender_views,
    x='gender',
    y='total_persons',
    title="Total Views by Gender",
    color='gender',
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Vivid
)
st.plotly_chart(gender_views_chart, use_container_width=True)

# Footer Section
st.markdown("---")
st.markdown("""
    <div class="footer">
        Developed with ❤️ using Streamlit and Plotly<br>
        Contact: <a href="owaisiqbal2928@gmail.com">owaisiqbal2928@gmail.com</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
